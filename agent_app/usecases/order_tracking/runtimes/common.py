"""Shared by the runtime modules: tool adapters, model choice, the loop contract, graph nodes."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Awaitable, Callable

from app import config

from .. import bus
from ..brain import CATEGORY, SYSTEM, actions_for, task_text
from ..standins import PolicyChatModel, PolicyLlm
from ..tools import RunRef, Tool, as_json, make_tools, step

KIND = {"heads_up": "out_for_delivery", "delivered": "delivered", "delay": "delay", "address": "address", "lost": "issue", "damaged": "issue"}
CATEGORIES = {"heads_up", "delivered", "delay", "address", "lost", "damaged", "routine"}


# ---------------- models ----------------
def lc_model(mode: str):  # noqa: ANN201
    if mode == "scripted":
        return PolicyChatModel()
    from langchain.chat_models import init_chat_model

    return init_chat_model(config.LC_MODEL)


def adk_model(mode: str, **kw):  # noqa: ANN003, ANN201
    if mode == "scripted":
        return PolicyLlm(**kw)
    if "/" in config.ADK_MODEL:
        from google.adk.models.lite_llm import LiteLlm

        return LiteLlm(model=config.ADK_MODEL)
    return config.ADK_MODEL


# ---------------- tools in each framework's shape ----------------
def lc_tools(tools: list[Tool]):  # noqa: ANN201
    from langchain_core.tools import StructuredTool
    from pydantic import create_model

    def runner(t: Tool):  # noqa: ANN202
        def run(**kw) -> str:  # noqa: ANN003
            return as_json(t.call(**kw))
        return run

    return [StructuredTool.from_function(func=runner(t), name=t.name, description=t.desc,
                                         args_schema=create_model(f"{t.name}_args", **{k: (v, ...) for k, v in t.params.items()}))
            for t in tools]


def adk_tools(tools: list[Tool]):  # noqa: ANN201
    from google.adk.tools.base_tool import BaseTool
    from google.genai import types

    kinds = {str: "STRING", int: "INTEGER", float: "NUMBER", bool: "BOOLEAN"}

    class AdkTool(BaseTool):
        def __init__(self, t: Tool):
            super().__init__(name=t.name, description=t.desc)
            self.t = t

        def _get_declaration(self) -> types.FunctionDeclaration:
            props = {k: types.Schema(type=kinds[v]) for k, v in self.t.params.items()}
            return types.FunctionDeclaration(name=self.name, description=self.description,
                                             parameters=types.Schema(type="OBJECT", properties=props, required=list(props)))

        async def run_async(self, *, args: dict, tool_context) -> dict:  # noqa: ANN001, ARG002
            out = self.t.call(**args)
            return out if isinstance(out, dict) else {"result": out}

    return [AdkTool(t) for t in tools]


def claude_server(tools: list[Tool]):  # noqa: ANN201
    from claude_agent_sdk import create_sdk_mcp_server, tool

    defs = []
    for t in tools:
        async def handler(args: dict, _t: Tool = t) -> dict:
            return {"content": [{"type": "text", "text": as_json(_t.call(**args))}]}
        defs.append(tool(t.name, t.desc, dict(t.params))(handler))
    return create_sdk_mcp_server("app", tools=defs)


def claude_options(tools: list[Tool], system: str, mode: str):  # noqa: ANN201
    from claude_agent_sdk import ClaudeAgentOptions

    from ..standins import PolicyCLI

    opts = ClaudeAgentOptions(system_prompt=system, mcp_servers={"app": claude_server(tools)} if tools else {},
                              allowed_tools=[f"mcp__app__{t.name}" for t in tools], tools=[],
                              model=None if mode == "scripted" else config.CLAUDE_MODEL)
    return opts, (PolicyCLI() if mode == "scripted" else None)


async def claude_ask(client, prompt: str) -> str:  # noqa: ANN001
    from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

    await client.query(prompt)
    final = ""
    async for m in client.receive_response():
        if isinstance(m, AssistantMessage):
            final = "".join(b.text for b in m.content if isinstance(b, TextBlock)) or final
        elif isinstance(m, ResultMessage) and m.result:
            final = m.result
    return final


async def claude_once(tools: list[Tool], system: str, prompt: str, mode: str) -> str:
    from claude_agent_sdk import ClaudeSDKClient

    opts, transport = claude_options(tools, system, mode)
    async with ClaudeSDKClient(options=opts, transport=transport) as c:
        return await claude_ask(c, prompt)


# ---------------- the looping agent's contract ----------------
@dataclass
class LoopIO:
    """What a looping agent needs from the outside world. The agent decides how to loop;
    LoopIO decides when there is news and when to stop."""
    who: str
    interval: float = 2.0                 # seconds to wait when there's nothing new
    max_iterations: int = 50
    idle_limit: int = 0                   # stop after N empty polls in a row (0 = never)
    batch: int = 25
    before_poll: Callable[[], object] | None = None     # tests and demos: advance the simulator
    on_iteration: Callable[[int, list, str], Awaitable[None] | None] | None = None
    iteration: int = 0
    idle: int = 0
    summaries: list = field(default_factory=list)

    def poll(self) -> list[dict]:
        if self.before_poll:
            self.before_poll()
        rows = bus.read(bus.EVENTS, bus.cursor(self.who), self.batch)
        if rows:
            bus.set_cursor(self.who, rows[-1][0])
        events = [e for _, e in rows]
        self.idle = 0 if events else self.idle + 1
        return events

    def should_stop(self) -> bool:
        return (bus.flag(f"stop:{self.who}") or self.iteration >= self.max_iterations
                or (self.idle_limit and self.idle >= self.idle_limit))

    def task(self, events: list[dict]) -> str:
        self.iteration += 1
        return task_text({"agent": "looping", "iteration": self.iteration, "events": events})

    def record(self, ref: RunRef, events: list[dict], summary: str) -> None:
        self.summaries.append(summary)
        step(ref, "iteration", f"iteration {self.iteration}", {"events": len(events)}, summary)


async def python_loop(io: LoopIO, ref: RunRef, think: Callable[[str], Awaitable[str]]) -> str:
    """The plain loop used by runtimes without a native loop construct: poll, think, record, wait."""
    import asyncio

    while not io.should_stop():
        events = io.poll()
        if not events:
            if io.should_stop():
                break
            await asyncio.sleep(io.interval)
            continue
        summary = await think(io.task(events))
        io.record(ref, events, summary)
    return f"{io.iteration} iterations. " + (io.summaries[-1] if io.summaries else "No events.")


# ---------------- the graph agent's nodes (shared logic) ----------------
def tools_by_name(ref: RunRef) -> dict[str, Tool]:
    return {t.name: t for t in make_tools(ref)}


def load(tb: dict[str, Tool], event: dict) -> dict:
    return {"order": tb["get_order"].call(order_id=event["order_id"]), "tracking": tb["get_tracking"].call(order_id=event["order_id"])}


def classify_prompt(event: dict) -> str:
    return task_text({"agent": "classify", "event": event})


def parse_category(text: str, event: dict) -> str:
    try:
        cat = json.loads(text[text.index("{"): text.rindex("}") + 1])["category"]
    except (ValueError, KeyError, TypeError):
        cat = next((c for c in CATEGORIES if c in (text or "").lower()), None)
    return cat if cat in CATEGORIES else CATEGORY.get(event["code"], "routine")


def draft_prompt(category: str, order: dict) -> str:
    return task_text({"agent": "draft", "category": category, "order": order})


def investigate(tb: dict[str, Tool], order: dict) -> dict:
    return tb["carrier_status"].call(order_id=order["order_id"])


def act(tb: dict[str, Tool], category: str, order: dict) -> list:
    return [tb[n].call(**a) for n, a in actions_for(category, order) if n != "notify_customer"]


def notify(tb: dict[str, Tool], category: str, order: dict, message: str) -> dict:
    return tb["notify_customer"].call(order_id=order["order_id"], kind=KIND[category], message=message.strip())


def route_after_classify(category: str) -> str:
    return {"routine": "finish", "heads_up": "draft", "delivered": "draft", "delay": "act", "address": "act",
            "lost": "investigate", "damaged": "investigate"}[category]


SYSTEM = SYSTEM


def graph_summary(event: dict, category: str, actions: list, notified: dict | None) -> str:
    oid = event["order_id"]
    if category == "routine":
        return f"#{oid} {event['code']}: routine scan, no action."
    bits = []
    for a in actions or []:
        if not isinstance(a, dict):
            continue
        if "ticket_id" in a:
            bits.append(f"ticket {a['ticket_id']}" + (" (already open)" if a.get("existing") else ""))
        elif "approval_id" in a:
            bits.append(f"approval {a['approval_id']} {a.get('status')}")
        elif a.get("blocked"):
            bits.append(f"blocked: {a['reason']}")
    if notified:
        bits.append("customer emailed" if notified.get("sent") else "email skipped (already sent)")
    return f"#{oid} {event['code']} -> {category}: " + (", ".join(bits) or "done") + "."
