"""LangChain Deep Agents 0.7.

harness  create_deep_agent with a 'carrier-investigator' subagent. For a lost or damaged parcel
         the main agent hands the investigation to the subagent through the task tool.
looping  one deep agent, one checkpointed thread for the whole session, so it remembers what it
         handled in earlier iterations.
graph    the LangGraph workflow, except lost/damaged parcels go to a deep-agent node that
         investigates and acts on its own. Deterministic where it can be, agentic where it must be.
"""

from __future__ import annotations

from deepagents import create_deep_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from app.runtimes.lc_common import final_text

from ..brain import task_text
from ..tools import make_tools
from . import lg
from .common import SYSTEM, graph_summary, lc_model, lc_tools, python_loop

CHECKPOINTER = MemorySaver()


def _investigator(tools):  # noqa: ANN001, ANN202
    return {"name": "carrier-investigator", "description": "Investigates a lost or damaged parcel end to end: carrier check, ticket, reship request, customer email.",
            "system_prompt": SYSTEM["investigator"], "tools": tools}


async def harness(ref, ask: str, mode: str) -> str:  # noqa: ANN001
    tools = lc_tools(make_tools(ref))
    agent = create_deep_agent(model=lc_model(mode), tools=tools, system_prompt=SYSTEM["harness"], subagents=[_investigator(tools)])
    r = await agent.ainvoke({"messages": [HumanMessage(task_text({"agent": "harness", "ask": ask, "delegate": True}))]})
    return final_text(r["messages"])


async def looping(ref, io, mode: str) -> str:  # noqa: ANN001
    agent = create_deep_agent(model=lc_model(mode), tools=lc_tools(make_tools(ref)), system_prompt=SYSTEM["looping"], checkpointer=CHECKPOINTER)
    cfg = {"configurable": {"thread_id": f"loop-{ref.run_id}"}, "recursion_limit": 200}

    async def think(task: str) -> str:
        r = await agent.ainvoke({"messages": [HumanMessage(task)]}, cfg)
        return final_text(r["messages"])

    return await python_loop(io, ref, think)


async def graph(ref, event: dict, mode: str) -> tuple[str, list]:  # noqa: ANN001
    tools = lc_tools(make_tools(ref))
    investigator = create_deep_agent(model=lc_model(mode), tools=tools, system_prompt=SYSTEM["investigator"])

    def deep(s: dict) -> dict:
        r = investigator.invoke({"messages": [HumanMessage(task_text({"agent": "investigator", "order_id": s["order"]["order_id"]}))]})
        return {"actions": [], "message": final_text(r["messages"])}

    s = await lg.build_graph(ref, mode, deep=deep).ainvoke({"event": event, "path": []})
    summary = s.get("message") if "deep_agent" in s["path"] else graph_summary(event, s["category"], s.get("actions", []), s.get("notified"))
    return summary, s["path"]
