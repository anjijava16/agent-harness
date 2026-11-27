"""Pieces shared by the Deep Agents and LangGraph runtimes."""

from __future__ import annotations

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import StructuredTool
from pydantic import create_model

from .. import config
from .base import RunCtx


class ScriptedChatModel(GenericFakeChatModel):
    """Replays AIMessages. Only the model is scripted; the framework runs for real."""

    def bind_tools(self, tools, **kwargs):  # noqa: ANN001, ANN003, ARG002
        return self


def script(ctx: RunCtx) -> list[AIMessage]:
    out = []
    for i, s in enumerate(ctx.steps):
        if s.calls:
            out.append(AIMessage(content="", tool_calls=[{"name": n, "args": a, "id": f"call_{i}_{j}"} for j, (n, a) in enumerate(s.calls)]))
        else:
            out.append(AIMessage(content=s.text or ""))
    return out


def model(ctx: RunCtx):  # noqa: ANN201
    if ctx.scripted:
        return ScriptedChatModel(messages=iter(script(ctx)))
    from langchain.chat_models import init_chat_model

    return init_chat_model(ctx.prefs.get("lc_model") or config.LC_MODEL)


def _runner(rt, name: str):  # noqa: ANN001, ANN202
    def run(**kw) -> str:  # noqa: ANN003
        return rt.invoke_json(name, kw)
    return run


def tools(ctx: RunCtx) -> list[StructuredTool]:
    out = []
    for t in ctx.uc.all_tools:
        schema = create_model(f"{t.name}_args", **{k: (v, ...) for k, v in t.params.items()})
        out.append(StructuredTool.from_function(func=_runner(ctx.tools, t.name), name=t.name, description=t.desc, args_schema=schema))
    return out


def final_text(messages) -> str:  # noqa: ANN001
    for m in reversed(messages):
        if isinstance(m, AIMessage) and not m.tool_calls:
            return m.content if isinstance(m.content, str) else " ".join(p.get("text", "") for p in m.content if isinstance(p, dict))
    return ""
