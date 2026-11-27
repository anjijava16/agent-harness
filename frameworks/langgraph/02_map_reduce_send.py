"""LangGraph: map-reduce fan-out with Send and a reducer.

Send(node, payload) schedules one run of `node` per item, in parallel. Each run returns a
partial update; the `Annotated[list, operator.add]` reducer merges them instead of
overwriting. This is how you process N things concurrently and collect the results.

Use case: draft a reminder for every overdue invoice at once, then build one summary.
"""

import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class State(TypedDict):
    invoices: list[dict]
    drafts: Annotated[list[str], operator.add]     # reducer: append, don't replace
    summary: str


class DraftInput(TypedDict):
    invoice: dict


def fan_out(state: State) -> list[Send]:
    return [Send("draft_one", {"invoice": inv}) for inv in state["invoices"] if inv["days"] > 0]


def draft_one(payload: DraftInput) -> dict:
    inv = payload["invoice"]
    return {"drafts": [f"{inv['id']}: Hi {inv['customer']}, ${inv['amount']} is {inv['days']}d overdue."]}


def summarize(state: State) -> dict:
    total = sum(i["amount"] for i in state["invoices"] if i["days"] > 0)
    return {"summary": f"{len(state['drafts'])} reminders drafted, ${total:,} outstanding"}


g = StateGraph(State)
g.add_node("draft_one", draft_one)
g.add_node("summarize", summarize)
g.add_conditional_edges(START, fan_out, ["draft_one"])
g.add_edge("draft_one", "summarize")
g.add_edge("summarize", END)
graph = g.compile()

if __name__ == "__main__":
    out = graph.invoke({"invoices": [
        {"id": "INV-1038", "customer": "Northwind", "amount": 2400, "days": 14},
        {"id": "INV-1042", "customer": "BrightPath", "amount": 850, "days": 3},
        {"id": "INV-1044", "customer": "Contoso", "amount": 1200, "days": 0},
        {"id": "INV-1050", "customer": "Fabrikam", "amount": 3100, "days": 22},
    ], "drafts": []})
    for d in out["drafts"]:
        print(" ", d)
    print(out["summary"])
