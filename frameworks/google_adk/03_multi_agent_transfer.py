"""Google ADK: LLM-driven delegation with sub_agents and transfer_to_agent.

Give an Agent sub_agents=[...] and ADK adds a transfer_to_agent tool automatically. The
coordinator's model decides who should handle the request; control moves to that agent
(and can move back). Each agent's `description` is what the coordinator reads to decide.

Compare with 04 (fixed workflow agents) and the ADK 2.0 Workflow graphs in
../google_adk_workflows, where code, not the model, picks the route.

Use case: a help desk where billing questions go to billing and everything else to support.
"""

import asyncio
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Agent  # noqa: E402

from frameworks._fakes.adk_fake import llm, run  # noqa: E402


def get_invoice(invoice_id: str) -> dict:
    """Fetch one invoice."""
    return {"id": invoice_id, "amount": 850, "status": "open", "pay_link": f"https://pay.acme.studio/{invoice_id}"}


billing = Agent(
    name="billing_agent", description="Handles invoices, payments, refunds and pay links.",
    model=llm(("tool", "get_invoice", {"invoice_id": "INV-1042"}),
              "INV-1042 is $850 and still open. Here's your link: https://pay.acme.studio/INV-1042"),
    instruction="Answer billing questions using get_invoice.", tools=[get_invoice],
)
support = Agent(name="support_agent", description="Handles product and account questions.",
                model=llm("Happy to help with your account."), instruction="General support.")

coordinator = Agent(
    name="help_desk", model=llm(("transfer", "billing_agent")),
    instruction="Route the user to the right specialist. Don't answer yourself.",
    sub_agents=[billing, support],
)

if __name__ == "__main__":
    asyncio.run(run(coordinator, "Can you resend the link for INV-1042?"))
