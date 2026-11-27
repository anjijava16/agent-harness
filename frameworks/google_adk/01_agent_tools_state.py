"""Google ADK 2.x: an Agent with tools, session state and output_key.

  from google.adk import Agent, Runner      (2.x top-level imports; google.adk.agents still works)
  tools        plain Python functions; docstring + type hints become the schema
  ToolContext  a tool can ask for `tool_context` to read/write session state
  output_key   the agent's final text is saved to session.state[output_key]
  Runner       binds the agent to a SessionService and yields Events

Use case: a finance agent that finds overdue invoices, records the total in state for
the next agent, and saves its answer under state["ar_summary"].

Run: python frameworks/google_adk/01_agent_tools_state.py        (offline, scripted model)
     GOOGLE_API_KEY=... python ... --live                          (Gemini)
"""

import asyncio
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Agent  # noqa: E402
from google.adk.tools import ToolContext  # noqa: E402

from frameworks._fakes.adk_fake import llm, run, state_of  # noqa: E402

INVOICES = [{"id": "INV-1038", "customer": "Northwind", "amount": 2400, "days": 14},
            {"id": "INV-1042", "customer": "BrightPath", "amount": 850, "days": 3}]


def list_overdue_invoices(min_days: int, tool_context: ToolContext) -> dict:
    """List open invoices overdue by at least min_days and remember the total."""
    rows = [i for i in INVOICES if i["days"] >= min_days]
    tool_context.state["ar_total"] = sum(r["amount"] for r in rows)   # visible to later agents
    return {"invoices": rows}


finance_agent = Agent(
    name="finance_agent",
    model=llm(("tool", "list_overdue_invoices", {"min_days": 1}),
              "Two invoices are overdue: Northwind $2,400 (14d) and BrightPath $850 (3d)."),
    instruction="You find overdue invoices. Always call list_overdue_invoices first.",
    tools=[list_overdue_invoices],
    output_key="ar_summary",
)


async def main() -> None:
    runner, session = await run(finance_agent, "What's overdue?")
    print("\nsession.state:", await state_of(runner, session))


if __name__ == "__main__":
    asyncio.run(main())
