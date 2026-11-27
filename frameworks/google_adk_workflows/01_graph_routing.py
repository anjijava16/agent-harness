"""ADK 2.0 Workflow: a graph of nodes with code-decided routing.

The big ADK 2.0 change: a Workflow is a graph engine. Agents, tools and plain functions are
all *nodes*. You declare edges as tuples:

    (START, a, b)                  chain: START -> a -> b
    (b, {"x": c, "y": d})          route: b sets ctx.route = "x" or "y"
    (START, (a, b))                fan-out to a and b in parallel

A node's return value becomes the next node's `node_input`. A node can take `ctx` to set
ctx.route or read/write ctx.state. Because the route is set in code, a confused or
prompt-injected model can't take a path you didn't draw.

Use case: the escalation ladder for overdue invoices, without a model at all.
"""

import asyncio
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Context, Workflow  # noqa: E402
from google.adk.workflow import START  # noqa: E402

from frameworks._fakes.adk_fake import run  # noqa: E402

LEDGER = {"INV-1042": 3, "INV-1038": 14, "INV-0990": 45}


def lookup(node_input) -> dict:  # noqa: ANN001
    inv = node_input.parts[0].text.strip()            # first node receives the user message
    return {"invoice": inv, "days": LEDGER[inv]}


def classify(ctx: Context, node_input: dict) -> dict:
    d = node_input["days"]
    ctx.route = "nudge" if d <= 7 else "firm" if d <= 30 else "human"
    ctx.state["last_route"] = ctx.route
    return node_input


def nudge(node_input: dict) -> str:
    return f"{node_input['invoice']}: friendly nudge drafted"


def firm(node_input: dict) -> str:
    return f"{node_input['invoice']}: firm reminder drafted"


def human(node_input: dict) -> str:
    return f"{node_input['invoice']}: escalated to the account owner"


workflow = Workflow(
    name="escalation_ladder",
    edges=[
        (START, lookup, classify),
        (classify, {"nudge": nudge, "firm": firm, "human": human}),
    ],
)


async def main() -> None:
    for inv in LEDGER:
        print(f"--- {inv}")
        await run(workflow, inv)


if __name__ == "__main__":
    asyncio.run(main())
