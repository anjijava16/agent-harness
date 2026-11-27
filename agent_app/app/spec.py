"""A framework-neutral way to describe a use case.

The same UseCase runs on Deep Agents, LangGraph, Google ADK or the Claude Agent SDK. It holds:
  tools      what the agent can call (canned data offline; swap `returns=` for a real call)
  steps      what a scripted model decides, turn by turn (only used in scripted mode)
  approvals  tools that pause for a person, and the decision used when auto-approving a demo
  guards     hard rules checked in code before a tool runs; they see the user's preferences
  prefs      defaults this use case needs; the user's own preferences win

Strings in step arguments and answers can use {placeholders} from the user's preferences, e.g.
call("get_weather", city="{home_city}"). Change home_city in the UI and the run follows.
"""

from __future__ import annotations

import copy
import itertools
import re
from dataclasses import dataclass, field
from typing import Any, Callable

_ids = itertools.count(1)


@dataclass
class T:
    name: str
    desc: str
    params: dict = field(default_factory=dict)      # arg name -> python type
    returns: Any = None                             # value, or callable(**args) -> value
    effect: str = "read"                            # read | write | external | money

    def compute(self, args: dict) -> Any:
        return self.returns(**args) if callable(self.returns) else copy.deepcopy(self.returns)


@dataclass
class Step:
    calls: list = field(default_factory=list)       # [(tool, args)]
    text: str | None = None                         # final answer


def call(name: str, /, **args) -> Step:  # noqa: ANN003
    return Step(calls=[(name, args)])


def par(*steps: Step) -> Step:
    """Several tool calls in one model turn."""
    return Step(calls=[c for s in steps for c in s.calls])


def remember(key: str, value: str) -> Step:
    return call("remember", key=key, value=value)


def recall(topic: str) -> Step:
    return call("recall", topic=topic)


def answer(text: str) -> Step:
    return Step(text=text)


MEMORY_TOOLS = [
    T("remember", "Save a fact or preference to the user's long-term memory.", {"key": str, "value": str}, effect="write"),
    T("recall", "Look up the user's long-term memory. Topic is a word or key prefix; empty returns everything.", {"topic": str}),
]


class _Safe(dict):
    def __missing__(self, k: str) -> str:
        return "{" + k + "}"


def fill(value: Any, prefs: dict) -> Any:
    if isinstance(value, str):
        try:
            return value.format_map(_Safe(prefs))
        except (ValueError, IndexError):
            return value
    if isinstance(value, dict):
        return {k: fill(v, prefs) for k, v in value.items()}
    if isinstance(value, list):
        return [fill(v, prefs) for v in value]
    return value


@dataclass
class UseCase:
    id: int
    area: str
    title: str
    ask: str
    why: str
    tools: list[T]
    steps: list[Step]
    approvals: dict = field(default_factory=dict)   # tool -> "approve" | "reject" | ("edit", {args}) | [one per call]
    guards: dict = field(default_factory=dict)      # tool -> fn(args, prefs) -> reason | None
    prefs: dict = field(default_factory=dict)
    expect: list = field(default_factory=list)      # [(label, fn(ctx) -> bool)]
    folder: str = ""

    @property
    def all_tools(self) -> list[T]:
        return self.tools + MEMORY_TOOLS

    @property
    def gated(self) -> set[str]:
        return set(self.approvals)

    def tool(self, name: str) -> T:
        return next(t for t in self.all_tools if t.name == name)

    def resolved(self, prefs: dict) -> tuple[str, list[Step]]:
        return fill(self.ask, prefs), [Step(calls=[(n, fill(a, prefs)) for n, a in s.calls], text=fill(s.text, prefs)) for s in self.steps]

    @property
    def features(self) -> list[str]:
        names = [n for s in self.steps for n, _ in s.calls]
        f = []
        if any(len(s.calls) > 1 for s in self.steps):
            f.append("parallel calls")
        if self.approvals:
            f.append("approval")
        if self.guards:
            f.append("guard")
        if "remember" in names or "recall" in names:
            f.append("memory")
        texts = [v for s in self.steps for _, a in s.calls for v in a.values() if isinstance(v, str)] + [self.ask] + [s.text or "" for s in self.steps]
        if any(re.search(r"\{[a-z_]+\}", t) for t in texts):
            f.append("uses preferences")
        return f


def scripted_decision(uc: UseCase, tool: str, nth: int, args: dict) -> dict:
    """The decision a demo run makes for the nth (0-based) gated call of `tool`."""
    d = uc.approvals.get(tool, "approve")
    if isinstance(d, list):
        d = d[nth] if nth < len(d) else d[-1]
    if d == "approve":
        return {"type": "approve"}
    if d == "reject":
        return {"type": "reject", "message": f"Not now, skip {tool}."}
    return {"type": "edit", "args": {**args, **d[1]}}


def system_prompt(uc: UseCase, prefs: dict) -> str:
    lines = "\n".join(f"- {k}: {v}" for k, v in prefs.items())
    return (f"You are the personal assistant of {prefs.get('name', 'the user')}. Task area: {uc.area}.\n"
            f"Use the tools to get real data; never make numbers up. Use recall/remember for long-term memory.\n"
            f"Some tools pause for the user's approval; some are blocked by policy. If a tool is blocked or rejected, "
            f"say so plainly and continue.\nThe user's preferences:\n{lines}\n")


Guard = Callable[[dict, dict], "str | None"]
