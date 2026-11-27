"""Scripted model for Google ADK (works with ADK 2.x Agent and Workflow).

ADK lets you pass any BaseLlm subclass as `model=`. This one replays a script:
    "text"                       -> a plain text reply
    ("tool", name, {args})       -> a function call
    ("transfer", agent_name)     -> ADK's built-in transfer_to_agent call
Pass --live to an example to use a real Gemini model instead (needs GOOGLE_API_KEY).
"""

from __future__ import annotations

import logging
import os
import sys
from typing import AsyncGenerator

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.genai import types

logging.getLogger("google_adk").setLevel(logging.CRITICAL)  # hide retry tracebacks and token-usage notes


class ScriptedLlm(BaseLlm):
    model: str = "scripted"
    script: list = []
    i: int = 0

    async def generate_content_async(self, llm_request, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:  # noqa: ANN001, ARG002
        item = self.script[self.i] if self.i < len(self.script) else "Done."
        self.i += 1
        if isinstance(item, tuple) and item[0] == "tool":
            part = types.Part(function_call=types.FunctionCall(name=item[1], args=item[2]))
        elif isinstance(item, tuple) and item[0] == "transfer":
            part = types.Part(function_call=types.FunctionCall(name="transfer_to_agent", args={"agent_name": item[1]}))
        else:
            part = types.Part(text=str(item))
        yield LlmResponse(content=types.Content(role="model", parts=[part]))


def llm(*script):
    """A real Gemini model name if --live, else a ScriptedLlm."""
    if "--live" in sys.argv:
        return os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    return ScriptedLlm(script=list(script))


def user(text: str) -> types.Content:
    return types.Content(role="user", parts=[types.Part(text=text)])


async def run(target, text: str, *, session=None, runner=None, quiet: bool = False):  # noqa: ANN001
    """Run an Agent or a Workflow once and print the interesting events. Returns (runner, session)."""
    from google.adk import Runner
    from google.adk.sessions import InMemorySessionService

    if runner is None:
        ss = InMemorySessionService()
        kind = {"node": target} if target.__class__.__name__ == "Workflow" else {"agent": target}
        runner = Runner(app_name="demo", session_service=ss, **kind)
        session = await ss.create_session(app_name="demo", user_id="me")
    msg = text if isinstance(text, types.Content) else user(text)
    async for ev in runner.run_async(user_id="me", session_id=session.id, new_message=msg):
        if quiet:
            continue
        parts = ev.content.parts if ev.content and ev.content.parts else []
        for p in parts:
            if p.function_call:
                print(f"  [{ev.author}] call {p.function_call.name}({str(dict(p.function_call.args or {}))[:150]})")
            elif p.function_response:
                print(f"  [{ev.author}] result {p.function_response.name}: {str(p.function_response.response)[:90]}")
            elif p.text:
                print(f"  [{ev.author}] {p.text[:110]}")
        if getattr(ev, "output", None) is not None and not parts:
            print(f"  [{ev.author}] output: {str(ev.output)[:110]}")
    return runner, session


async def state_of(runner, session) -> dict:  # noqa: ANN001
    s = await runner.session_service.get_session(app_name="demo", user_id="me", session_id=session.id)
    return dict(s.state)
