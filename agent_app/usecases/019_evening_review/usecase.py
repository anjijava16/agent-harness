"""Evening review

Area: mornings
Reads this morning's goal from memory and compares it with what you actually finished.

Run:  python usecases/019_evening_review/usecase.py                  # your preferred framework
      python usecases/019_evening_review/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/019_evening_review/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=19,
    area="mornings",
    title="Evening review",
    ask="Do my evening review.",
    why="Reads this morning's goal from memory and compares it with what you actually finished.",
    tools=[T("done_tasks", "Tasks completed today.", {"day": str}, ["Expense report", "Report draft"])],
    steps=[par(recall("goal_today"), call("done_tasks", day="today")),
           answer("You hit today's goal: the report draft is done, and the expense report too.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
