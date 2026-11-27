"""LangChain 1.x structured output with response_format.

Two strategies:
  ProviderStrategy  uses the provider's native JSON-schema mode (when the model supports it)
  ToolStrategy      exposes the schema as a tool the model must call; works with any
                    tool-calling model. Passing a bare Pydantic class lets LangChain pick.

The validated object lands in result["structured_response"].

Use case: email triage. Turn a messy inbound email into a typed ticket your code can route.
"""

import pathlib
import sys
from typing import Literal

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from langchain.agents import create_agent  # noqa: E402
from langchain.agents.structured_output import ToolStrategy  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from frameworks._fakes.lc_fake import call, model  # noqa: E402


class TriagedEmail(BaseModel):
    """A triaged inbound email."""
    category: Literal["payment_promise", "dispute", "resend_request", "other"]
    invoice_id: str | None = Field(description="Invoice mentioned, if any")
    urgency: Literal["low", "medium", "high"]
    next_action: str


agent = create_agent(
    model=model(call("TriagedEmail", {"category": "resend_request", "invoice_id": "INV-1042",
                                      "urgency": "medium", "next_action": "Resend INV-1042 with pay link"})),
    tools=[],
    response_format=ToolStrategy(TriagedEmail),
    system_prompt="Triage accounts-receivable email.",
)

if __name__ == "__main__":
    email = "Hi! Sorry, this slipped. Can you resend the invoice? (re: INV-1042) - Maria"
    r = agent.invoke({"messages": [{"role": "user", "content": email}]})
    t: TriagedEmail = r["structured_response"]
    print("typed result:", repr(t))
    route = {"resend_request": "billing-queue", "dispute": "human-review", "payment_promise": "calendar-follow-up"}
    print("route to:", route.get(t.category, "inbox"))
