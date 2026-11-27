"""Google ADK: callbacks as guardrails.

  before_model_callback(callback_context, llm_request)  -> LlmResponse | None
      return a response to skip the model entirely (input guardrail, caching)
  before_tool_callback(tool, args, tool_context)        -> dict | None
      return a dict to skip the real tool; the dict becomes the tool result (approval gate)
  after_tool_callback(tool, args, tool_context, tool_response) -> dict | None
      rewrite or redact a tool result before the model sees it

Use case: block card numbers in user input, require approval for sending, and mask
customer emails in tool output.
"""

import asyncio
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Agent  # noqa: E402
from google.adk.models.llm_response import LlmResponse  # noqa: E402
from google.genai import types  # noqa: E402

from frameworks._fakes.adk_fake import llm, run  # noqa: E402

SENT: list[str] = []
CARD = re.compile(r"\b(?:\d[ -]?){13,16}\b")


def lookup_customer(name: str) -> dict:
    """Look up a customer's billing contact."""
    return {"name": name, "email": "ap@northwind.com", "terms": "net 30"}


def send_email(to: str, body: str) -> dict:
    """Send an email to a customer."""
    SENT.append(to)
    return {"status": "sent", "to": to}


def block_card_numbers(callback_context, llm_request):  # noqa: ANN001
    last = llm_request.contents[-1] if llm_request.contents else None
    text = " ".join(p.text or "" for p in (last.parts if last else []))
    if CARD.search(text):
        return LlmResponse(content=types.Content(role="model", parts=[types.Part(
            text="I can't process card numbers in chat. Please use the secure payment link.")]))
    return None


def approve_sends(tool, args, tool_context):  # noqa: ANN001, ARG001
    if tool.name == "send_email" and not args.get("to", "").endswith("@northwind.com"):
        return {"status": "blocked", "reason": f"{args.get('to')} not approved"}
    return None


def mask_emails(tool, args, tool_context, tool_response):  # noqa: ANN001, ARG001
    if tool.name == "lookup_customer" and isinstance(tool_response, dict) and "email" in tool_response:
        return {**tool_response, "email": tool_response["email"][0] + "***@" + tool_response["email"].split("@")[1]}
    return None


def make_agent(script):  # noqa: ANN001
    return Agent(
        name="collections", model=llm(*script), instruction="Chase overdue invoices politely.",
        tools=[lookup_customer, send_email],
        before_model_callback=block_card_numbers,
        before_tool_callback=approve_sends,
        after_tool_callback=mask_emails,
    )


async def main() -> None:
    print("== 1. input guardrail: card number never reaches the model ==")
    await run(make_agent(["(the model would have answered here)"]), "Charge my card 4242 4242 4242 4242 for INV-1038")

    print("\n== 2. tool guardrails: masked lookup, one send allowed, one blocked ==")
    await run(make_agent([
        ("tool", "lookup_customer", {"name": "Northwind"}),
        ("tool", "send_email", {"to": "ap@northwind.com", "body": "Friendly nudge on INV-1038"}),
        ("tool", "send_email", {"to": "random@gmail.com", "body": "fyi"}),
        "Northwind reminded; the gmail send was blocked.",
    ]), "Remind Northwind and cc my gmail")
    print("\nactually sent:", SENT)


if __name__ == "__main__":
    asyncio.run(main())
