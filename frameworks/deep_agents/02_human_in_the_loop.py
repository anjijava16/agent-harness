"""Deep Agents: interrupt_on for approvals, with reject feedback.

interrupt_on maps tool names to True or {"allowed_decisions": [...]}. A checkpointer is
required so the paused run can be resumed. A rejection's `message` goes back to the model,
so it can adjust instead of retrying blindly.

Use case: the agent wants to delete old notes and send a reminder. You let the email go
and stop the delete.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from deepagents import create_deep_agent  # noqa: E402
from langchain.tools import tool  # noqa: E402
from langgraph.checkpoint.memory import MemorySaver  # noqa: E402
from langgraph.types import Command  # noqa: E402

from frameworks._fakes.lc_fake import calls, model, say, show  # noqa: E402

OUTBOX: list[str] = []


@tool
def send_email(to: str, body: str) -> str:
    """Send an email to a customer."""
    OUTBOX.append(to)
    return f"sent to {to}"


@tool
def purge_notes(older_than_days: int) -> str:
    """Delete notes older than N days. Irreversible."""
    return f"purged notes older than {older_than_days}d"


agent = create_deep_agent(
    model=model(
        calls(("send_email", {"to": "ap@northwind.com", "body": "Friendly nudge on INV-1038"}),
              ("purge_notes", {"older_than_days": 7})),
        say("Reminder sent. I left the notes alone as you asked."),
    ),
    tools=[send_email, purge_notes],
    interrupt_on={
        "send_email": {"allowed_decisions": ["approve", "reject"]},
        "purge_notes": True,                  # True = approve / edit / reject allowed
    },
    checkpointer=MemorySaver(),
)

if __name__ == "__main__":
    cfg = {"configurable": {"thread_id": "hitl-1"}}
    r = agent.invoke({"messages": [{"role": "user", "content": "Chase Northwind and tidy up old notes"}]}, cfg)
    while r.get("__interrupt__"):
        req = r["__interrupt__"][0].value
        decisions = []
        for action in req["action_requests"]:
            if action["name"] == "send_email":
                decisions.append({"type": "approve"})
            else:
                decisions.append({"type": "reject", "message": "Keep notes for 90 days; don't purge."})
            print(f"  {action['name']}({action['args']}) -> {decisions[-1]['type']}")
        r = agent.invoke(Command(resume={"decisions": decisions}), cfg)
    show(r["messages"][-3:])
    print("outbox:", OUTBOX)
