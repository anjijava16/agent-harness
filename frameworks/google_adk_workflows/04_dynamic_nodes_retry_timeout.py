"""ADK 2.0 Workflow: dynamic nodes, retries and timeouts.

* Dynamic nodes: inside a node, `await ctx.run_node(other, node_input=...)` runs another
  node at runtime. Ordinary Python loops and if/else become workflow control flow. The
  parent must be @node(rerun_on_resume=True) so it can pick up child results after a pause.
* RetryConfig(max_attempts, initial_delay, max_delay, backoff_factor, jitter, exceptions)
  on @node(retry_config=...) retries a failing node with backoff.
* @node(timeout=seconds) fails a node that runs too long (NodeTimeoutError).

Use case: a payment-provider API that fails twice before answering, and a reminder that
gets improved in a loop until it's short enough.
"""

import asyncio
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Context, Workflow  # noqa: E402
from google.adk.workflow import START, RetryConfig, node  # noqa: E402

from frameworks._fakes.adk_fake import run  # noqa: E402

CALLS = {"stripe": 0}


@node(retry_config=RetryConfig(max_attempts=4, initial_delay=0.01, backoff_factor=2.0))
def fetch_stripe_status(node_input) -> dict:  # noqa: ANN001, ARG001
    CALLS["stripe"] += 1
    if CALLS["stripe"] < 3:
        raise ConnectionError("stripe 503")
    return {"invoice": "INV-1038", "status": "open", "attempts": CALLS["stripe"]}


def shorten(node_input: dict) -> dict:
    words = node_input["text"].split()
    return {**node_input, "text": " ".join(words[: max(8, len(words) - 6)]), "rounds": node_input["rounds"] + 1}


@node(rerun_on_resume=True)
async def improve_until_short(ctx: Context, node_input: dict) -> dict:
    draft = {"text": ("Hello there Northwind team, we hope you are doing very well today and we wanted to "
                      "kindly remind you that invoice INV-1038 is now fourteen days overdue, thanks"),
             "rounds": 0, "status": node_input["status"]}
    while len(draft["text"].split()) > 12 and draft["rounds"] < 5:   # plain Python loop
        draft = await ctx.run_node(shorten, node_input=draft)
    return draft


@node(timeout=1.0)
async def finalize(node_input: dict) -> str:
    return f"{node_input['rounds']} rounds -> '{node_input['text']}'"


workflow = Workflow(name="resilient_reminder", edges=[(START, fetch_stripe_status, improve_until_short, finalize)])


async def main() -> None:
    await run(workflow, "go")
    print(f"\nstripe attempts: {CALLS['stripe']} (2 failures retried by RetryConfig)")


if __name__ == "__main__":
    asyncio.run(main())
