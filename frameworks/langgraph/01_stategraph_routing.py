"""LangGraph 1.x: StateGraph with conditional routing.

The mental model: state (a TypedDict) flows through nodes (functions that return partial
state updates); edges decide what runs next. Conditional edges are plain Python, so the
route is deterministic and testable. No model is needed to show the mechanics.

Use case: invoice escalation ladder.
    <=7 days  -> friendly nudge
    8-30 days -> firm reminder
    >30 days  -> hand to a human
"""

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    invoice: dict
    action: str
    log: list[str]


def assess(state: State) -> dict:
    return {"log": state.get("log", []) + [f"assessed {state['invoice']['id']} ({state['invoice']['days']}d)"]}


def route(state: State) -> Literal["nudge", "firm", "human"]:
    d = state["invoice"]["days"]
    return "nudge" if d <= 7 else "firm" if d <= 30 else "human"


def nudge(state: State) -> dict:
    return {"action": "friendly nudge drafted", "log": state["log"] + ["nudge"]}


def firm(state: State) -> dict:
    return {"action": "firm reminder drafted", "log": state["log"] + ["firm"]}


def human(state: State) -> dict:
    return {"action": "escalated to account owner", "log": state["log"] + ["human"]}


g = StateGraph(State)
g.add_node("assess", assess)
for name, fn in [("nudge", nudge), ("firm", firm), ("human", human)]:
    g.add_node(name, fn)
    g.add_edge(name, END)
g.add_edge(START, "assess")
g.add_conditional_edges("assess", route)
graph = g.compile()

if __name__ == "__main__":
    for inv in [{"id": "INV-1042", "days": 3}, {"id": "INV-1038", "days": 14}, {"id": "INV-0990", "days": 45}]:
        out = graph.invoke({"invoice": inv, "log": []})
        print(f"{inv['id']:>9}: {out['action']:<28} path={out['log']}")
    print("\nMermaid of the graph:\n" + graph.get_graph().draw_mermaid())
