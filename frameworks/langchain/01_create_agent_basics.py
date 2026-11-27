"""LangChain 1.x: create_agent basics.

create_agent replaced langgraph.prebuilt.create_react_agent as the standard way to build an
agent. It returns a compiled LangGraph graph, so invoke/stream/checkpointers all work.

Use case: an AR (accounts receivable) assistant that looks up overdue invoices and drafts
reminders.

Run:  python frameworks/langchain/01_create_agent_basics.py          (offline)
      LC_MODEL=anthropic:claude-sonnet-4-6 python ... --live          (real model)
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from langchain.agents import create_agent  # noqa: E402
from langchain.tools import tool  # noqa: E402

from frameworks._fakes.lc_fake import call, model, say, show  # noqa: E402

INVOICES = [{"id": "INV-1038", "customer": "Northwind", "amount": 2400, "days": 14},
            {"id": "INV-1042", "customer": "BrightPath", "amount": 850, "days": 3}]


@tool
def list_overdue_invoices(min_days: int = 1) -> list[dict]:
    """List open invoices at least `min_days` overdue."""
    return [i for i in INVOICES if i["days"] >= min_days]


@tool
def draft_reminder(invoice_id: str, tone: str = "friendly") -> str:
    """Draft a payment reminder for one invoice. Doesn't send anything."""
    inv = next(i for i in INVOICES if i["id"] == invoice_id)
    return f"[{tone}] Hi {inv['customer']}, {invoice_id} (${inv['amount']}) is {inv['days']} days overdue."


agent = create_agent(
    model=model(
        call("list_overdue_invoices", {"min_days": 7}),
        call("draft_reminder", {"invoice_id": "INV-1038", "tone": "friendly"}),
        say("One invoice is over a week late: Northwind INV-1038. I drafted a friendly reminder."),
    ),
    tools=[list_overdue_invoices, draft_reminder],
    system_prompt="You are an AR assistant. Draft, never send.",
)

if __name__ == "__main__":
    print("== invoke ==")
    result = agent.invoke({"messages": [{"role": "user", "content": "Anything more than a week overdue?"}]})
    show(result["messages"])
    print("\n== the agent is a LangGraph graph ==")
    print("  nodes:", list(agent.get_graph().nodes))
