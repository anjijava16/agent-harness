"""LangChain 1.x middleware: the part that makes create_agent production-ready.

Middleware hooks into the agent loop: before/after the model call, around each tool call,
and around the whole agent. This file stacks five of them:

  PIIMiddleware               redact emails from user input before the model sees them
  @dynamic_prompt             change the system prompt per request (here: by user tier)
  @wrap_tool_call (custom)    a Sentinel-style egress check: block non-customer domains
  ToolCallLimitMiddleware     at most 2 send_email calls per run
  HumanInTheLoopMiddleware    pause before send_email; resume with approve / edit / reject

Use case: a collections agent that must never email the wrong person.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import (HumanInTheLoopMiddleware, ModelRequest, PIIMiddleware,  # noqa: E402
                                         ToolCallLimitMiddleware, dynamic_prompt, wrap_tool_call)
from langchain.tools import tool  # noqa: E402
from langchain_core.messages import ToolMessage  # noqa: E402
from langgraph.checkpoint.memory import InMemorySaver  # noqa: E402
from langgraph.types import Command  # noqa: E402

from frameworks._fakes.lc_fake import call, calls, model, say, show  # noqa: E402

SENT: list[dict] = []
ALLOWED = ("@northwind.com", "@brightpath.io")


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a customer."""
    SENT.append({"to": to, "subject": subject})
    return f"sent to {to}"


@dynamic_prompt
def tiered_prompt(request: ModelRequest) -> str:
    tier = (request.runtime.context or {}).get("tier", "standard") if request.runtime else "standard"
    return f"You chase overdue invoices. Customer tier: {tier}. Be {'very gentle' if tier == 'vip' else 'friendly'}."


@wrap_tool_call
def egress_guard(request, handler):  # noqa: ANN001
    """Runs around every tool call. Deterministic; never reads model text."""
    if request.tool_call["name"] == "send_email":
        to = request.tool_call["args"].get("to", "")
        if not to.endswith(ALLOWED):
            return ToolMessage(content=f"BLOCKED: {to} is not a customer domain",
                               tool_call_id=request.tool_call["id"], name="send_email")
    return handler(request)


def build():
    return create_agent(
        model=model(
            calls(("send_email", {"to": "ap@northwind.com", "subject": "INV-1038", "body": "Friendly nudge"}),
                  ("send_email", {"to": "me@gmail.com", "subject": "copy", "body": "cc myself"})),
            say("Northwind reminder handled; the gmail copy was blocked."),
        ),
        tools=[send_email],
        middleware=[
            PIIMiddleware("email", strategy="redact", apply_to_input=True),
            tiered_prompt,
            egress_guard,
            ToolCallLimitMiddleware(tool_name="send_email", run_limit=2),
            HumanInTheLoopMiddleware(interrupt_on={
                "send_email": {"allowed_decisions": ["approve", "edit", "reject"]}}),
        ],
        checkpointer=InMemorySaver(),   # HITL needs somewhere to park the paused run
    )


if __name__ == "__main__":
    agent = build()
    cfg = {"configurable": {"thread_id": "collections-1"}}
    print("== run until the human-in-the-loop pause ==")
    r = agent.invoke({"messages": [{"role": "user", "content": "Remind maria@brightpath.io and Northwind about their invoices"}]},
                     cfg, context={"tier": "vip"})
    print("  user text after PII redaction:", r["messages"][0].content)
    for req in r["__interrupt__"][0].value["action_requests"]:
        print("  needs approval:", req["name"], req["args"])

    print("\n== resume: edit the first (soften subject), approve the second ==")
    decisions = [
        {"type": "edit", "edited_action": {"name": "send_email",
                                           "args": {"to": "ap@northwind.com", "subject": "Quick note on INV-1038",
                                                    "body": "Friendly nudge"}}},
        {"type": "approve"},
    ]
    r = agent.invoke(Command(resume={"decisions": decisions}), cfg, context={"tier": "vip"})
    show(r["messages"])
    print("\n  actually sent:", SENT)
