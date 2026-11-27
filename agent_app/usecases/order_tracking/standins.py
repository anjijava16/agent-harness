"""Stand-in models that let every runtime run offline, driven by brain.decide().

  PolicyChatModel  a LangChain chat model  -> LangChain, LangGraph, Deep Agents
  PolicyLlm        an ADK BaseLlm          -> ADK agents and ADK workflow agent nodes
  PolicyCLI        a Claude Agent SDK Transport that speaks the CLI's side of the protocol

Each one rebuilds (task, observations) from its framework's own message format, asks the brain,
and answers in that framework's format. The frameworks themselves run unmodified.
"""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any, AsyncGenerator

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from app.runtimes.claude_rt import ScriptedCLI

from .brain import decide, parse_task

logging.getLogger("google_adk").setLevel(logging.ERROR)   # stand-in models report no token usage; ADK logs that


def _loads(x: Any) -> Any:  # noqa: ANN401
    if isinstance(x, str):
        try:
            return json.loads(x)
        except ValueError:
            return x
    return x


# ---------------- LangChain family ----------------
class PolicyChatModel(BaseChatModel):
    @property
    def _llm_type(self) -> str:
        return "policy"

    def bind_tools(self, tools, **kwargs):  # noqa: ANN001, ANN003, ARG002
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:  # noqa: ANN001, ANN003, ARG002
        idx = max(i for i, m in enumerate(messages) if isinstance(m, HumanMessage))
        content = messages[idx].content
        text = content if isinstance(content, str) else " ".join(b.get("text", "") for b in content if isinstance(b, dict))
        task, calls, obs = parse_task(text), {}, []
        for m in messages[idx + 1:]:
            if isinstance(m, AIMessage):
                calls.update({tc["id"]: tc for tc in m.tool_calls})
            elif isinstance(m, ToolMessage):
                tc = calls.get(m.tool_call_id, {})
                obs.append({"tool": m.name or tc.get("name"), "args": tc.get("args", {}), "result": _loads(m.content)})
        d = decide(task, obs)
        if "final" in d:
            msg = AIMessage(content=d["final"])
        else:
            msg = AIMessage(content="", tool_calls=[{"name": n, "args": a, "id": f"call_{uuid.uuid4().hex[:10]}"} for n, a in d["calls"]])
        return ChatResult(generations=[ChatGeneration(message=msg)])


# ---------------- Google ADK ----------------
class PolicyLlm(BaseLlm):
    model: str = "policy"
    role: str = ""          # optional override, e.g. "coordinator" in the ADK agent tree

    async def generate_content_async(self, llm_request, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:  # noqa: ANN001, ARG002
        contents = llm_request.contents or []
        idx = max((i for i, c in enumerate(contents) if c.role == "user" and any(p.text and "TASK:" in p.text for p in (c.parts or []))), default=0)
        text = " ".join(p.text for p in (contents[idx].parts or []) if p.text) if contents else ""
        task, calls, obs = parse_task(text), [], []
        for c in contents[idx + 1:]:
            for p in c.parts or []:
                if p.function_call:
                    calls.append(p.function_call)
                elif p.function_response:
                    # pair by id when ids survive, otherwise the first unanswered call with that name
                    fr = p.function_response
                    fc = next((x for x in calls if fr.id and x.id == fr.id), None) or next((x for x in calls if x.name == fr.name), None)
                    if fc is not None:
                        calls.remove(fc)
                    resp = fr.response or {}
                    result = resp["result"] if set(resp) == {"result"} else resp
                    obs.append({"tool": p.function_response.name, "args": dict(fc.args or {}) if fc else {}, "result": result})
        d = self.decide(task, obs)
        if "final" in d:
            parts = [types.Part(text=d["final"])]
        else:
            parts = [types.Part(function_call=types.FunctionCall(name=n, args=a)) for n, a in d["calls"]]
        yield LlmResponse(content=types.Content(role="model", parts=parts))

    def decide(self, task: dict, obs: list) -> dict:
        return decide(task, obs)


# ---------------- Claude Agent SDK ----------------
class PolicyCLI(ScriptedCLI):
    """Plays the `claude` CLI. Each query (user message) runs one brain-driven agent loop:
    assistant tool_use -> MCP tools/call on the app's in-process server -> tool_result -> ... -> result."""

    def __init__(self):
        super().__init__([])
        self.prompt = ""

    async def write(self, data: str) -> None:
        for line in data.splitlines():
            if line.strip():
                m = json.loads(line)
                if m.get("type") == "user":
                    c = m["message"]["content"]
                    self.prompt = c if isinstance(c, str) else " ".join(b.get("text", "") for b in c if isinstance(b, dict))
        await super().write(data)

    async def _play(self) -> None:
        sid, task, obs, turns = "policy", parse_task(self.prompt), [], 0
        while True:
            turns += 1
            d = decide(task, obs)
            if "final" in d or turns > 12:
                final = d.get("final", "Stopped after 12 turns.")
                await self.send.send({"type": "assistant", "session_id": sid, "message": {"model": "policy", "content": [{"type": "text", "text": final}]}})
                await self.send.send({"type": "result", "subtype": "success", "duration_ms": 0, "duration_api_ms": 0, "is_error": False,
                                      "num_turns": turns, "session_id": sid, "result": final})
                return
            uses = [(f"toolu_{uuid.uuid4().hex[:10]}", n, a) for n, a in d["calls"]]
            await self.send.send({"type": "assistant", "session_id": sid, "message": {"model": "policy", "content": [
                {"type": "tool_use", "id": tid, "name": f"mcp__app__{n}", "input": a} for tid, n, a in uses]}})
            if not self.mcp_ready:
                await self._mcp("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "policy-cli", "version": "1"}})
                await self._mcp("notifications/initialized", notify=True)
                self.mcp_ready = True
            results = []
            for tid, n, a in uses:                       # all tools are pre-allowed (allowed_tools), as the real CLI would see them
                r = await self._mcp("tools/call", {"name": n, "arguments": a})
                content = r.get("mcp_response", {}).get("result", {}).get("content", [{"type": "text", "text": json.dumps(r)}])
                obs.append({"tool": n, "args": a, "result": _loads(content[0].get("text", "")) if content else None})
                results.append({"type": "tool_result", "tool_use_id": tid, "content": content})
            await self.send.send({"type": "user", "session_id": sid, "message": {"role": "user", "content": results}})
