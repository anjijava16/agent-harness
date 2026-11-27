"""LangChain 1.x.

harness  create_agent + TodoListMiddleware: a harness assembled from LangChain's own parts
looping  the same kind of agent, called once per batch of events from a plain Python loop
graph    an LCEL pipeline: RunnableLambda nodes and a RunnableBranch for routing
"""

from __future__ import annotations

from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableBranch, RunnableLambda

from app.runtimes.lc_common import final_text

from ..brain import task_text
from ..tools import make_tools, step
from .common import (SYSTEM, act, classify_prompt, draft_prompt, graph_summary, investigate, lc_model, lc_tools, load, notify,
                     parse_category, python_loop, tools_by_name)


async def harness(ref, ask: str, mode: str) -> str:  # noqa: ANN001
    agent = create_agent(lc_model(mode), lc_tools(make_tools(ref)), system_prompt=SYSTEM["harness"], middleware=[TodoListMiddleware()])
    r = await agent.ainvoke({"messages": [HumanMessage(task_text({"agent": "harness", "ask": ask}))]})
    return final_text(r["messages"])


async def looping(ref, io, mode: str) -> str:  # noqa: ANN001
    agent = create_agent(lc_model(mode), lc_tools(make_tools(ref)), system_prompt=SYSTEM["looping"])

    async def think(task: str) -> str:
        r = await agent.ainvoke({"messages": [HumanMessage(task)]})
        return final_text(r["messages"])

    return await python_loop(io, ref, think)


async def graph(ref, event: dict, mode: str) -> tuple[str, list]:  # noqa: ANN001
    tb, model, path = tools_by_name(ref), lc_model(mode), []

    def node(name: str, fn):  # noqa: ANN001, ANN202
        def run(s: dict) -> dict:
            path.append(name)
            step(ref, "node", name)
            return fn(s)
        return RunnableLambda(run)

    def ask(system: str, prompt: str) -> str:
        return model.invoke([SystemMessage(system), HumanMessage(prompt)]).content

    load_n = node("load", lambda s: {**s, **load(tb, s["event"])})
    classify_n = node("classify", lambda s: {**s, "category": parse_category(ask(SYSTEM["classify"], classify_prompt(s["event"])), s["event"])})
    investigate_n = node("investigate", lambda s: {**s, "carrier": investigate(tb, s["order"])})
    act_n = node("act", lambda s: {**s, "actions": act(tb, s["category"], s["order"])})
    draft_n = node("draft", lambda s: {**s, "message": ask(SYSTEM["draft"], draft_prompt(s["category"], s["order"]))})
    notify_n = node("notify", lambda s: {**s, "notified": notify(tb, s["category"], s["order"], s["message"])})
    finish_n = node("finish", lambda s: s)
    tail = draft_n | notify_n | finish_n
    chain = load_n | classify_n | RunnableBranch(
        (lambda s: s["category"] == "routine", finish_n),
        (lambda s: s["category"] in ("heads_up", "delivered"), tail),
        (lambda s: s["category"] in ("lost", "damaged"), investigate_n | act_n | tail),
        act_n | tail,
    )
    s = await chain.ainvoke({"event": event})
    return graph_summary(event, s["category"], s.get("actions", []), s.get("notified")), path
