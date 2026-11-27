"""Claude Agent SDK: tools are an in-process MCP server; approvals go through can_use_tool.

can_use_tool is a callback the SDK awaits, so a paused run is a coroutine waiting for the
user's decision. The decision is handed over through Redis (cache.push_decisions /
wait_decisions), which is also how it would reach the right worker in a bigger deployment.

Scripted mode swaps the Claude Code CLI for ScriptedCLI, a Transport that speaks the CLI's
side of the stream-json control protocol. Everything on the SDK side is real: the client, the
permission callback and the MCP tool server."""

from __future__ import annotations

import asyncio
import itertools
import json
import warnings

import anyio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    PermissionResultAllow,
    PermissionResultDeny,
    ResultMessage,
    TextBlock,
    create_sdk_mcp_server,
    tool,
)
from claude_agent_sdk._internal.transport import Transport

from .. import cache, config
from .base import Outcome, RunCtx, Runtime

SERVER = "app"
# Intended: ungated tools are pre-allowed via allowed_tools, so the callback only sees gated ones.
warnings.filterwarnings("ignore", message=".*can_use_tool.*")


def _full(name: str) -> str:
    return f"mcp__{SERVER}__{name}"


class ScriptedCLI(Transport):
    """Stands in for the `claude` CLI process and plays the use case's steps."""

    def __init__(self, steps):  # noqa: ANN001
        self.steps = steps
        self.send, self.recv = anyio.create_memory_object_stream(1000)
        self.waiting: dict[str, list] = {}
        self.ids = itertools.count(1)
        self.ready = False
        self.mcp_ready = False
        self.player: asyncio.Task | None = None

    async def connect(self) -> None:
        self.ready = True

    def is_ready(self) -> bool:
        return self.ready

    async def end_input(self) -> None:
        pass

    async def close(self) -> None:
        self.ready = False
        if self.player and not self.player.done():
            self.player.cancel()
        await self.send.aclose()

    async def read_messages(self):  # noqa: ANN201
        async with self.recv:
            async for m in self.recv:
                yield m

    async def write(self, data: str) -> None:
        for line in data.splitlines():
            if not line.strip():
                continue
            m = json.loads(line)
            if m["type"] == "control_request":           # initialize, etc.
                await self.send.send({"type": "control_response", "response": {"subtype": "success", "request_id": m["request_id"], "response": {}}})
            elif m["type"] == "control_response":        # answers to our can_use_tool / mcp_message
                r = m["response"]
                slot = self.waiting.get(r["request_id"])
                if slot:
                    slot[1] = r.get("response", {}) if r.get("subtype") == "success" else {"error": r.get("error")}
                    slot[0].set()
            elif m["type"] == "user":
                self.player = asyncio.get_running_loop().create_task(self._play())

    async def _ask(self, request: dict) -> dict:
        rid = f"cli_{next(self.ids)}"
        slot = [anyio.Event(), None]
        self.waiting[rid] = slot
        await self.send.send({"type": "control_request", "request_id": rid, "request": request})
        await slot[0].wait()
        return self.waiting.pop(rid)[1]

    async def _mcp(self, method: str, params: dict | None = None, notify: bool = False) -> dict:
        msg = {"jsonrpc": "2.0", "method": method, **({"params": params} if params is not None else {})}
        if not notify:
            msg["id"] = next(self.ids)
        return await self._ask({"subtype": "mcp_message", "server_name": SERVER, "message": msg})

    async def _play(self) -> None:
        sid, last = "scripted", ""
        for s in self.steps:
            if not s.calls:
                last = s.text or ""
                await self.send.send({"type": "assistant", "message": {"model": "scripted", "content": [{"type": "text", "text": last}]}, "session_id": sid})
                continue
            uses = [(f"toolu_{next(self.ids)}", n, a) for n, a in s.calls]
            await self.send.send({"type": "assistant", "session_id": sid, "message": {"model": "scripted", "content": [
                {"type": "tool_use", "id": tid, "name": _full(n), "input": a} for tid, n, a in uses]}})
            if not self.mcp_ready:                       # the MCP handshake the real CLI does first
                await self._mcp("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "scripted-cli", "version": "1"}})
                await self._mcp("notifications/initialized", notify=True)
                self.mcp_ready = True
            results = []
            for tid, n, a in uses:
                perm = await self._ask({"subtype": "can_use_tool", "tool_name": _full(n), "input": a, "tool_use_id": tid})
                if perm.get("behavior") == "allow":
                    r = await self._mcp("tools/call", {"name": n, "arguments": perm.get("updatedInput", a)})
                    content = r.get("mcp_response", {}).get("result", {}).get("content", [{"type": "text", "text": str(r)}])
                else:
                    content = [{"type": "text", "text": "Denied: " + perm.get("message", "")}]
                results.append({"type": "tool_result", "tool_use_id": tid, "content": content})
            await self.send.send({"type": "user", "session_id": sid, "message": {"role": "user", "content": results}})
        await self.send.send({"type": "result", "subtype": "success", "duration_ms": 0, "duration_api_ms": 0, "is_error": False,
                              "num_turns": len(self.steps), "session_id": sid, "result": last})


def _mcp_server(ctx: RunCtx):  # noqa: ANN201
    defs = []
    for t in ctx.uc.all_tools:
        async def handler(args: dict, _name: str = t.name) -> dict:
            return {"content": [{"type": "text", "text": ctx.tools.invoke_json(_name, args)}]}
        defs.append(tool(t.name, t.desc, dict(t.params))(handler))
    return create_sdk_mcp_server(SERVER, tools=defs)


class ClaudeRuntime(Runtime):
    name = "claude"

    async def start(self, ctx: RunCtx) -> Outcome:
        self.q: asyncio.Queue[Outcome] = asyncio.Queue()
        self.task = asyncio.get_running_loop().create_task(self._main(ctx))
        return await self.q.get()

    async def resume(self, ctx: RunCtx, decisions: list[dict]) -> Outcome:
        cache.push_decisions(ctx.run_id, decisions)
        return await self.q.get()

    async def _main(self, ctx: RunCtx) -> None:
        gated = ctx.uc.gated

        async def can_use_tool(name: str, inp: dict, context):  # noqa: ANN001, ANN202
            t = name.removeprefix(f"mcp__{SERVER}__")
            if t not in gated:
                return PermissionResultAllow()
            await self.q.put(Outcome("paused", pending=[{"id": context.tool_use_id or t, "tool": t, "args": inp}]))
            got = await cache.wait_decisions(ctx.run_id)
            d = (got or [{"type": "reject", "message": "no decision in time"}])[0]
            if d["type"] == "reject":
                return PermissionResultDeny(message=d.get("message", "The user declined."))
            if d["type"] == "edit":
                return PermissionResultAllow(updated_input=d["args"])
            return PermissionResultAllow()

        opts = ClaudeAgentOptions(
            system_prompt=ctx.prompt,
            mcp_servers={SERVER: _mcp_server(ctx)},
            allowed_tools=[_full(t.name) for t in ctx.uc.all_tools if t.name not in gated],
            tools=[],                                     # no built-in Bash/Read/Edit: only our tools
            can_use_tool=can_use_tool,
            model=None if ctx.scripted else (ctx.prefs.get("claude_model") or config.CLAUDE_MODEL),
        )
        transport = ScriptedCLI(ctx.steps) if ctx.scripted else None
        final = ""
        try:
            async with ClaudeSDKClient(options=opts, transport=transport) as client:
                await client.query(ctx.ask)
                async for m in client.receive_response():
                    if isinstance(m, AssistantMessage):
                        text = "".join(b.text for b in m.content if isinstance(b, TextBlock))
                        final = text or final
                    elif isinstance(m, ResultMessage) and m.result:
                        final = m.result
            await self.q.put(Outcome("done", final=final))
        except Exception as e:  # noqa: BLE001
            await self.q.put(Outcome("error", error=f"{type(e).__name__}: {e}"))
