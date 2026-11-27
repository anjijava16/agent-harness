"""Scripted chat model for LangChain / LangGraph / Deep Agents.

GenericFakeChatModel ships with langchain-core. It replays a list of AIMessages. We add
bind_tools() so create_agent / create_deep_agent accept it, and two helpers to build the
messages a real model would have returned.
"""

from __future__ import annotations

import os
import sys

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage


class ScriptedChatModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):  # noqa: ANN001, ANN003, ARG002
        return self


def call(name: str, args: dict | None = None, id: str | None = None) -> AIMessage:  # noqa: A002
    """An AI turn that requests one tool call."""
    return AIMessage(content="", tool_calls=[{"name": name, "args": args or {}, "id": id or f"call_{name}"}])


def calls(*items: tuple[str, dict]) -> AIMessage:
    """An AI turn that requests several tool calls in parallel."""
    return AIMessage(content="", tool_calls=[{"name": n, "args": a, "id": f"call_{n}_{i}"} for i, (n, a) in enumerate(items)])


def say(text: str) -> AIMessage:
    return AIMessage(content=text)


def model(*turns: AIMessage):
    """Return a real model if --live was passed (LC_MODEL, e.g. 'anthropic:claude-sonnet-4-6'),
    otherwise a scripted one that replays `turns`."""
    if "--live" in sys.argv:
        from langchain.chat_models import init_chat_model

        return init_chat_model(os.environ.get("LC_MODEL", "anthropic:claude-sonnet-4-6"))
    return ScriptedChatModel(messages=iter(list(turns)))


def show(messages) -> None:  # noqa: ANN001
    for m in messages:
        tc = getattr(m, "tool_calls", None)
        if tc:
            print(f"  {m.type:>5}: -> " + ", ".join(f"{t['name']}({t['args']})" for t in tc))
        else:
            content = m.content if isinstance(m.content, str) else str(m.content)
            name = f" [{m.name}]" if getattr(m, "name", None) else ""
            print(f"  {m.type:>5}{name}: {content[:110]}")
