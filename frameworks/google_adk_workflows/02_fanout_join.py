"""ADK 2.0 Workflow: parallel fan-out and JoinNode fan-in.

    (START, (a, b, c))        a, b, c run concurrently
    ((a, b, c), join)         a JoinNode waits for all predecessors
    (join, report)            the join's output is {"a": ..., "b": ..., "c": ...}

Use case: before a collections call, gather payment history, contract terms and recent
emails in parallel, then build one briefing.
"""

import asyncio
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Workflow  # noqa: E402
from google.adk.workflow import START, JoinNode  # noqa: E402

from frameworks._fakes.adk_fake import run  # noqa: E402


async def payment_history(node_input) -> str:  # noqa: ANN001, ARG001
    await asyncio.sleep(0.05)
    return "3 late payments in 2026, all settled within 10 days of a nudge"


async def contract_terms(node_input) -> str:  # noqa: ANN001, ARG001
    await asyncio.sleep(0.05)
    return "net 30, 1.5% monthly late fee"


async def recent_emails(node_input) -> str:  # noqa: ANN001, ARG001
    await asyncio.sleep(0.05)
    return "AP said on Nov 20 that payment is 'in the next run'"


def briefing(node_input: dict) -> str:
    lines = [f"- {k.replace('_', ' ')}: {v}" for k, v in node_input.items()]
    return "Northwind call briefing\n" + "\n".join(lines)


gather = JoinNode(name="gather")
workflow = Workflow(
    name="call_briefing",
    edges=[
        (START, (payment_history, contract_terms, recent_emails)),
        ((payment_history, contract_terms, recent_emails), gather),
        (gather, briefing),
    ],
)


async def main() -> None:
    import time

    t = time.perf_counter()
    await run(workflow, "brief me on Northwind")
    print(f"\nthree 50 ms lookups finished in {(time.perf_counter() - t) * 1000:.0f} ms (parallel)")


if __name__ == "__main__":
    asyncio.run(main())
