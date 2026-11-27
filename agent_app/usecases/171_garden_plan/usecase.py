"""Plan the spring garden

Area: learning
Uses your growing zone and what grew well last year (saved in memory).

Run:  python usecases/171_garden_plan/usecase.py                  # your preferred framework
      python usecases/171_garden_plan/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/171_garden_plan/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=171,
    area="learning",
    title="Plan the spring garden",
    ask="What should I plant this spring?",
    why="Uses your growing zone and what grew well last year (saved in memory).",
    tools=[T("planting_calendar", "Planting calendar for a zone.", {"zone": str}, {"start_indoors_march": ["tomatoes", "peppers"], "direct_sow_may": ["beans", "zucchini"]})],
    steps=[recall("garden"), call("planting_calendar", zone="6a"),
           answer("Start tomatoes and peppers indoors in March, and sow beans and zucchini directly in May.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
