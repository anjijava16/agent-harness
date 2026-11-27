"""LangGraph 1.x, everything drawn as a graph.

harness  agent <-> tools ReAct graph, built by hand (START -> agent -> tools -> agent -> END)
looping  the loop is the graph: poll -> agent <-> tools -> record -> poll, with a wait node when
         there's nothing new. One invocation runs until LoopIO says stop.
graph    StateGraph: load -> classify -> (route) -> investigate -> act -> draft -> notify -> finish
"""

from __future__ import annotations

import asyncio
import operator
from typing import Annotated, Callable, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage, SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.message import REMOVE_ALL_MESSAGES, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from app.runtimes.lc_common import final_text

from ..brain import task_text
from ..tools import make_tools, step
from .common import (SYSTEM, act, classify_prompt, draft_prompt, graph_summary, investigate, lc_model, lc_tools, load, notify,
                     parse_category, route_after_classify, tools_by_name)


def react(model, tools, system: str):  # noqa: ANN001, ANN201
    llm = model.bind_tools(tools)
    g = StateGraph(MessagesState)
    g.add_node("agent", lambda s: {"messages": [llm.invoke([SystemMessage(system), *s["messages"]])]})
    g.add_node("tools", ToolNode(tools))
    g.add_edge(START, "agent")
    g.add_conditional_edges("agent", tools_condition)
    g.add_edge("tools", "agent")
    return g.compile()


async def harness(ref, ask: str, mode: str) -> str:  # noqa: ANN001
    app = react(lc_model(mode), lc_tools(make_tools(ref)), SYSTEM["harness"])
    r = await app.ainvoke({"messages": [HumanMessage(task_text({"agent": "harness", "ask": ask}))]})
    return final_text(r["messages"])


class LoopState(TypedDict):
    messages: Annotated[list, add_messages]
    events: list


async def looping(ref, io, mode: str) -> str:  # noqa: ANN001
    tools = lc_tools(make_tools(ref))
    llm = lc_model(mode).bind_tools(tools)

    def poll(s: LoopState) -> dict:
        if io.should_stop():
            return {"events": []}
        events = io.poll()
        if not events:
            return {"events": []}
        # fresh context each iteration: drop the last batch's messages
        return {"events": events, "messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), HumanMessage(io.task(events))]}

    def after_poll(s: LoopState) -> str:
        return "agent" if s["events"] else (END if io.should_stop() else "wait")

    async def wait(s: LoopState) -> dict:
        await asyncio.sleep(io.interval)
        return {}

    def agent(s: LoopState) -> dict:
        return {"messages": [llm.invoke([SystemMessage(SYSTEM["looping"]), *s["messages"]])]}

    def after_agent(s: LoopState) -> str:
        last = s["messages"][-1]
        return "tools" if isinstance(last, AIMessage) and last.tool_calls else "record"

    def record(s: LoopState) -> dict:
        io.record(ref, s["events"], final_text(s["messages"]))
        return {"events": []}

    g = StateGraph(LoopState)
    for name, fn in [("poll", poll), ("wait", wait), ("agent", agent), ("tools", ToolNode(tools)), ("record", record)]:
        g.add_node(name, fn)
    g.add_edge(START, "poll")
    g.add_conditional_edges("poll", after_poll, ["agent", "wait", END])
    g.add_edge("wait", "poll")
    g.add_conditional_edges("agent", after_agent, ["tools", "record"])
    g.add_edge("tools", "agent")
    g.add_edge("record", "poll")
    await g.compile().ainvoke({"messages": [], "events": []}, {"recursion_limit": 100_000})
    return f"{io.iteration} iterations. " + (io.summaries[-1] if io.summaries else "No events.")


class GState(TypedDict, total=False):
    event: dict
    order: dict
    tracking: list
    category: str
    actions: list
    message: str
    notified: dict
    path: Annotated[list, operator.add]


def build_graph(ref, mode: str, deep: Callable[[dict], dict] | None = None):  # noqa: ANN001, ANN201
    """deep: optional node that handles lost/damaged parcels on its own (used by the Deep Agents runtime)."""
    tb, model = tools_by_name(ref), lc_model(mode)

    def ask(system: str, prompt: str) -> str:
        return model.invoke([SystemMessage(system), HumanMessage(prompt)]).content

    def n(name: str, fn):  # noqa: ANN001, ANN202
        def run(s: GState) -> dict:
            step(ref, "node", name)
            return {**fn(s), "path": [name]}
        return run

    nodes = {
        "load": lambda s: load(tb, s["event"]),
        "classify": lambda s: {"category": parse_category(ask(SYSTEM["classify"], classify_prompt(s["event"])), s["event"])},
        "investigate": lambda s: {"actions": [investigate(tb, s["order"])]},
        "act": lambda s: {"actions": (s.get("actions") or []) + act(tb, s["category"], s["order"])},
        "draft": lambda s: {"message": ask(SYSTEM["draft"], draft_prompt(s["category"], s["order"]))},
        "notify": lambda s: {"notified": notify(tb, s["category"], s["order"], s["message"])},
        "finish": lambda s: {},
    }
    g = StateGraph(GState)
    for name, fn in nodes.items():
        g.add_node(name, n(name, fn))
    targets = ["finish", "draft", "act", "investigate"]
    if deep:
        g.add_node("deep_agent", n("deep_agent", deep))
        targets.append("deep_agent")
    g.add_edge(START, "load")
    g.add_edge("load", "classify")

    def route(s: GState) -> str:
        nxt = route_after_classify(s["category"])
        return "deep_agent" if deep and nxt == "investigate" else nxt

    g.add_conditional_edges("classify", route, targets)
    g.add_edge("investigate", "act")
    g.add_edge("act", "draft")
    g.add_edge("draft", "notify")
    g.add_edge("notify", "finish")
    if deep:
        g.add_edge("deep_agent", "finish")
    g.add_edge("finish", END)
    return g.compile()


async def graph(ref, event: dict, mode: str) -> tuple[str, list]:  # noqa: ANN001
    s = await build_graph(ref, mode).ainvoke({"event": event, "path": []})
    return graph_summary(event, s["category"], s.get("actions", []), s.get("notified")), s["path"]
