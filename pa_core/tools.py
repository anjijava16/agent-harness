"""Tools: the agent's hands.

A tool is a Python function plus metadata the agent loop and the policy layer need:
a JSON schema for the model, and a risk level for the approval gate.

Risk levels follow the pattern almost every personal agent ships with:

    READ      -> look but don't touch (read inbox, search web). Usually auto-approved.
    WRITE     -> changes your own stuff (create a draft, add a calendar block).
    EXTERNAL  -> other people see it (send email, post to Slack, call someone).
    MONEY     -> spends money (checkout, pay invoice).

OpenAI Dots, for example, restricts unprompted background research to read-only tools,
and Copilot Cowork asks before every action. Both are just policies over these levels.
"""

from __future__ import annotations

import inspect
import json
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Callable, get_type_hints


class Risk(IntEnum):
    READ = 0
    WRITE = 1
    EXTERNAL = 2
    MONEY = 3


_PY_TO_JSON = {str: "string", int: "integer", float: "number", bool: "boolean",
               list: "array", dict: "object"}


@dataclass
class Tool:
    name: str
    description: str
    fn: Callable[..., Any]
    risk: Risk = Risk.READ
    parameters: dict = field(default_factory=dict)

    def schema(self) -> dict:
        """OpenAI-style function schema (also accepted by xAI, Perplexity, OpenClaw...)."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def __call__(self, **kwargs: Any) -> Any:
        return self.fn(**kwargs)


def _schema_from_signature(fn: Callable[..., Any]) -> dict:
    sig = inspect.signature(fn)
    hints = get_type_hints(fn)
    props, required = {}, []
    for name, param in sig.parameters.items():
        if name in ("self", "ctx"):
            continue
        typ = hints.get(name, str)
        props[name] = {"type": _PY_TO_JSON.get(typ, "string")}
        if param.default is inspect.Parameter.empty:
            required.append(name)
    return {"type": "object", "properties": props, "required": required}


def tool(name: str | None = None, *, risk: Risk = Risk.READ, description: str | None = None):
    """Decorator: turn a plain function into a Tool."""

    def wrap(fn: Callable[..., Any]) -> Tool:
        return Tool(
            name=name or fn.__name__,
            description=(description or inspect.getdoc(fn) or fn.__name__).strip(),
            fn=fn,
            risk=risk,
            parameters=_schema_from_signature(fn),
        )

    return wrap


class ToolRegistry:
    def __init__(self, tools: list[Tool] | None = None):
        self._tools: dict[str, Tool] = {}
        for t in tools or []:
            self.add(t)

    def add(self, t: Tool) -> None:
        self._tools[t.name] = t

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"unknown tool: {name}")
        return self._tools[name]

    def names(self) -> list[str]:
        return list(self._tools)

    def schemas(self) -> list[dict]:
        return [t.schema() for t in self._tools.values()]

    def subset(self, max_risk: Risk) -> "ToolRegistry":
        """Registry limited to tools at or below a risk level (e.g. read-only research)."""
        return ToolRegistry([t for t in self._tools.values() if t.risk <= max_risk])

    def __contains__(self, name: str) -> bool:
        return name in self._tools

    def __len__(self) -> int:
        return len(self._tools)


def to_text(result: Any) -> str:
    if isinstance(result, str):
        return result
    try:
        return json.dumps(result, default=str)
    except TypeError:
        return str(result)
