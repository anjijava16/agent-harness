"""ADK 2.0 Workflow: LLM agents as nodes, used only where language is needed.

An Agent placed in a Workflow is just another node. Agent `mode` matters:
  "chat"         classic conversational agent (default for sub_agents)
  "single_turn"  answer once from its input and hand back to the graph; no transfers
  "task"         finish via a finish_task call with structured output (Task API)

The pattern Google recommends in "Why we built ADK 2.0": deterministic nodes for routing and
side effects, single-turn agents for the steps that need judgment. The agent classifies,
code routes. Google's illustrative benchmark measured ~50% fewer tokens and ~20% less latency
than one big agent doing everything.

Use case: support inbox triage. An LLM labels the email; code decides what happens next.
"""

import asyncio
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Agent, Context, Workflow  # noqa: E402
from google.adk.workflow import START  # noqa: E402

from frameworks._fakes.adk_fake import llm, run  # noqa: E402


def make_triage(label: str) -> Agent:
    return Agent(
        name="triage", mode="single_turn", model=llm(label),
        instruction=("Classify the email as exactly one word: payment_promise, dispute, or resend_request. "
                     "Reply with the word only."),
    )


def route(ctx: Context, node_input) -> str:  # noqa: ANN001
    label = str(node_input).strip().lower()
    ctx.route = label if label in {"payment_promise", "dispute", "resend_request"} else "dispute"
    return label


def schedule_follow_up(node_input) -> str:  # noqa: ANN001, ARG001
    return "follow-up scheduled for Friday"


def open_dispute_ticket(node_input) -> str:  # noqa: ANN001, ARG001
    return "dispute ticket opened for a human"


def resend_invoice(node_input) -> str:  # noqa: ANN001, ARG001
    return "invoice resent with pay link"


def build(label: str) -> Workflow:
    return Workflow(name="inbox_triage", edges=[
        (START, make_triage(label), route),
        (route, {"payment_promise": schedule_follow_up, "dispute": open_dispute_ticket,
                 "resend_request": resend_invoice}),
    ])


async def main() -> None:
    emails = [("We'll pay INV-1038 on Friday.", "payment_promise"),
              ("Can you resend INV-1042?", "resend_request"),
              ("We never received these goods.", "dispute")]
    for text, scripted_label in emails:
        print(f"--- {text}")
        await run(build(scripted_label), text)


if __name__ == "__main__":
    asyncio.run(main())
