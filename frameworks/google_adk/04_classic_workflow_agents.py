"""Google ADK: the classic workflow agents (deprecated in ADK 2.x, still working).

  SequentialAgent  run sub-agents in order, passing data through session.state
  ParallelAgent    run sub-agents concurrently (each writes its own output_key)
  LoopAgent        repeat sub-agents until max_iterations or one of them escalates

These were ADK 1.x's only deterministic orchestration. In ADK 2.15 they raise a
DeprecationWarning: "deprecated in favor of Workflow and will be removed in a future
version. Workflow cannot yet be used as an LlmAgent sub-agent." So: use Workflow graphs
(../google_adk_workflows) for new code, keep these for existing projects and for the one
case Workflow can't cover yet (nesting under an LlmAgent as a sub-agent).

Use case: research in parallel -> write a draft -> loop a critic until the draft passes.
"""

import asyncio
import pathlib
import sys
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module=__name__)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Agent  # noqa: E402
from google.adk.agents import LoopAgent, ParallelAgent, SequentialAgent  # noqa: E402
from google.adk.tools import ToolContext  # noqa: E402

from frameworks._fakes.adk_fake import llm, run, state_of  # noqa: E402


def approve_draft(tool_context: ToolContext) -> dict:
    """Call when the draft is good enough. Ends the review loop."""
    tool_context.actions.escalate = True
    return {"approved": True}


history = Agent(name="history", model=llm("Northwind paid late 3 times this year."), output_key="history",
                instruction="Summarize payment history.")
terms = Agent(name="terms", model=llm("Contract terms: net 30, 1.5% late fee."), output_key="terms",
              instruction="Summarize contract terms.")
research = ParallelAgent(name="research", sub_agents=[history, terms])

writer = Agent(name="writer", model=llm("Draft: Hi Northwind, INV-1038 is 14 days late; a 1.5% fee applies after 30."),
               output_key="draft", instruction="Write a reminder using {history} and {terms}.")

critic = Agent(name="critic", model=llm("Too stiff. Soften the opening.", ("tool", "approve_draft", {}), "Approved."),
               instruction="Review {draft}. Call approve_draft when it's friendly and accurate.",
               tools=[approve_draft])
reviser = Agent(name="reviser", model=llm("Draft: Hi Northwind team! Quick nudge: INV-1038 is 14 days late."),
                output_key="draft", instruction="Revise {draft} based on the critique.")
review_loop = LoopAgent(name="review_loop", sub_agents=[critic, reviser], max_iterations=3)

pipeline = SequentialAgent(name="reminder_pipeline", sub_agents=[research, writer, review_loop])


async def main() -> None:
    runner, session = await run(pipeline, "Prepare a reminder for Northwind")
    s = await state_of(runner, session)
    print("\nfinal state keys:", sorted(s))
    print("final draft:", s.get("draft"))


if __name__ == "__main__":
    asyncio.run(main())
