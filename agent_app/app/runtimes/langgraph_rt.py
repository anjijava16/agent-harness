"""LangGraph, built by hand: agent -> approval gate (interrupt) -> tools -> agent.

The gate node has no side effects, so re-running it on resume is safe. It asks once for all
gated calls in a turn, the same shape Deep Agents uses."""

from __future__ import annotations

from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.types import Command, interrupt

from . import lc_common
from .base import Outcome, RunCtx, Runtime

CHECKPOINTER = MemorySaver()


def build_graph(ctx: RunCtx):  # noqa: ANN201
    llm = lc_common.model(ctx)
    tools = lc_common.tools(ctx)
    llm_t = llm.bind_tools(tools)
    gated = ctx.uc.gated

    def agent(state: MessagesState) -> dict:
        return {"messages": [llm_t.invoke([SystemMessage(ctx.prompt), *state["messages"]])]}

    def gate(state: MessagesState) -> dict:
        last: AIMessage = state["messages"][-1]
        asks = [tc for tc in last.tool_calls if tc["name"] in gated]
        if not asks:
            return {}
        resp = interrupt({"action_requests": [{"name": tc["name"], "args": tc["args"], "id": tc["id"]} for tc in asks]})
        by_id = dict(zip([tc["id"] for tc in asks], resp["decisions"], strict=True))
        keep, notes = [], []
        for tc in last.tool_calls:
            d = by_id.get(tc["id"], {"type": "approve"})
            if d["type"] == "reject":
                notes.append(ToolMessage(content=f"Rejected by the user: {d.get('message', '')}", tool_call_id=tc["id"], name=tc["name"]))
            elif d["type"] == "edit":
                keep.append({**tc, "args": d["args"]})
            else:
                keep.append(tc)
        # Same id -> add_messages replaces the AI turn, so the tool node only sees approved calls.
        return {"messages": [AIMessage(content=last.content, tool_calls=keep, id=last.id), *notes]}

    def after_agent(state: MessagesState) -> str:
        return "gate" if state["messages"][-1].tool_calls else END

    def after_gate(state: MessagesState) -> str:
        # Rejection notes may follow the AI turn, so look at the latest AI message itself.
        ai = next(m for m in reversed(state["messages"]) if isinstance(m, AIMessage))
        return "tools" if ai.tool_calls else "agent"

    g = StateGraph(MessagesState)
    g.add_node("agent", agent)
    g.add_node("gate", gate)
    g.add_node("tools", ToolNode(tools))
    g.add_edge(START, "agent")
    g.add_conditional_edges("agent", after_agent, ["gate", END])
    g.add_conditional_edges("gate", after_gate, ["tools", "agent"])
    g.add_edge("tools", "agent")
    return g.compile(checkpointer=CHECKPOINTER)


class LangGraphRuntime(Runtime):
    name = "langgraph"

    async def start(self, ctx: RunCtx) -> Outcome:
        self.graph = build_graph(ctx)
        self.cfg = {"configurable": {"thread_id": ctx.run_id}, "recursion_limit": 60}
        return self._outcome(await self.graph.ainvoke({"messages": [{"role": "user", "content": ctx.ask}]}, self.cfg))

    async def resume(self, ctx: RunCtx, decisions: list[dict]) -> Outcome:
        return self._outcome(await self.graph.ainvoke(Command(resume={"decisions": decisions}), self.cfg))

    def _outcome(self, r: dict) -> Outcome:
        if r.get("__interrupt__"):
            req = r["__interrupt__"][0].value
            return Outcome("paused", pending=[{"id": a["id"], "tool": a["name"], "args": a["args"]} for a in req["action_requests"]])
        return Outcome("done", final=lc_common.final_text(r["messages"]))
