"""Outline a presentation

Area: work
Pulls the numbers and saves an outline.

Run:  python usecases/146_presentation_outline/usecase.py                  # your preferred framework
      python usecases/146_presentation_outline/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/146_presentation_outline/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=146,
    area="work",
    title="Outline a presentation",
    ask="Outline a 10-minute talk on our Q4 results.",
    why="Pulls the numbers and saves an outline.",
    tools=[T("q4_numbers", "Q4 figures.", {"team": str}, {"revenue_growth": "12%", "churn": "3.1%", "nps": 46})],
    steps=[call("q4_numbers", team="mine"), remember("talk_q4", "1 headline 12% growth; 2 churn 3.1%; 3 NPS 46; 4 next quarter"),
           answer("Four parts: 12% growth, churn at 3.1%, NPS of 46, then the plan for next quarter. Outline saved.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
