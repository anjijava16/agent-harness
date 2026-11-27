"""Google ADK 2.x: an Agent whose gated tools ask for confirmation. The App is resumable, so a
paused invocation picks up where it stopped once the confirmation arrives."""

from __future__ import annotations

import logging
from typing import AsyncGenerator

from google.adk.agents import Agent
from google.adk.apps import App, ResumabilityConfig
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.base_tool import BaseTool
from google.genai import types

from .. import config
from .base import Outcome, RunCtx, Runtime

logging.getLogger("google_adk").setLevel(logging.ERROR)

_T = {str: "STRING", int: "INTEGER", float: "NUMBER", bool: "BOOLEAN", list: "ARRAY", dict: "OBJECT"}
CONFIRM = "adk_request_confirmation"
# Process-wide. In production use DatabaseSessionService(db_url=...) so sessions live in your database.
SESSIONS = InMemorySessionService()


class ScriptedLlm(BaseLlm):
    """Replays the use case's steps. Several calls in one step come back as parallel function calls."""

    model: str = "scripted"
    turns: list = []
    i: int = 0

    async def generate_content_async(self, llm_request, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:  # noqa: ANN001, ARG002
        s = self.turns[self.i] if self.i < len(self.turns) else None
        self.i += 1
        if s is None or not s.calls:
            parts = [types.Part(text=(s.text if s else "") or "Done.")]
        else:
            parts = [types.Part(function_call=types.FunctionCall(name=n, args=a)) for n, a in s.calls]
        yield LlmResponse(content=types.Content(role="model", parts=parts))


class SpecTool(BaseTool):
    """One use-case tool. Gated tools use ADK's own confirmation flow (request_confirmation)."""

    def __init__(self, ctx: RunCtx, t):  # noqa: ANN001
        super().__init__(name=t.name, description=t.desc)
        self.ctx, self.t, self.gated = ctx, t, t.name in ctx.uc.gated

    def _get_declaration(self) -> types.FunctionDeclaration:
        props = {k: types.Schema(type=_T.get(v, "STRING")) for k, v in self.t.params.items()}
        return types.FunctionDeclaration(name=self.name, description=self.description,
                                         parameters=types.Schema(type="OBJECT", properties=props, required=list(props)))

    async def run_async(self, *, args: dict, tool_context) -> dict:  # noqa: ANN001
        if self.gated:
            c = tool_context.tool_confirmation
            if c is None:
                tool_context.request_confirmation(hint=f"Approve {self.name}?", payload={"args": args})
                tool_context.actions.skip_summarization = True
                return {"error": "waiting for the user's approval"}
            if not c.confirmed:
                return {"error": "rejected by the user"}
            if isinstance(c.payload, dict) and c.payload.get("edited_args"):
                args = c.payload["edited_args"]
        r = self.ctx.tools.invoke(self.name, dict(args))
        return r if isinstance(r, dict) else {"result": r}


def _model(ctx: RunCtx):  # noqa: ANN201
    if ctx.scripted:
        return ScriptedLlm(turns=ctx.steps)
    name = ctx.prefs.get("adk_model") or config.ADK_MODEL
    if "/" in name:                                  # e.g. anthropic/claude-sonnet-5-5 or openrouter/... via LiteLLM
        from google.adk.models.lite_llm import LiteLlm

        return LiteLlm(model=name)
    return name


class AdkRuntime(Runtime):
    name = "adk"

    async def start(self, ctx: RunCtx) -> Outcome:
        agent = Agent(name="assistant", model=_model(ctx), instruction=ctx.prompt, tools=[SpecTool(ctx, t) for t in ctx.uc.all_tools])
        app = App(name="agent_app", root_agent=agent, resumability_config=ResumabilityConfig(is_resumable=True))
        self.runner = Runner(app=app, session_service=SESSIONS)
        await SESSIONS.create_session(app_name="agent_app", user_id=ctx.user_id, session_id=ctx.run_id)
        return await self._run(ctx, types.Content(role="user", parts=[types.Part(text=ctx.ask)]))

    async def resume(self, ctx: RunCtx, decisions: list[dict]) -> Outcome:
        parts = []
        for p, d in zip(self.pending, decisions, strict=True):
            resp = {"confirmed": d["type"] != "reject"}
            if d["type"] == "edit":
                resp["payload"] = {"edited_args": d["args"]}
            parts.append(types.Part(function_response=types.FunctionResponse(name=CONFIRM, id=p["id"], response=resp)))
        return await self._run(ctx, types.Content(role="user", parts=parts), self.invocation_id)

    async def _run(self, ctx: RunCtx, msg: types.Content, invocation_id: str | None = None) -> Outcome:
        pending, final = [], ""
        async for ev in self.runner.run_async(user_id=ctx.user_id, session_id=ctx.run_id, new_message=msg, invocation_id=invocation_id):
            self.invocation_id = ev.invocation_id
            for part in (ev.content.parts if ev.content and ev.content.parts else []):
                fc = part.function_call
                if fc and fc.name == CONFIRM:
                    orig = fc.args["originalFunctionCall"]
                    pending.append({"id": fc.id, "tool": orig["name"], "args": dict(orig.get("args") or {})})
                elif part.text and not part.thought:
                    final = part.text
        if pending:
            self.pending = pending
            return Outcome("paused", pending=pending)
        return Outcome("done", final=final)
