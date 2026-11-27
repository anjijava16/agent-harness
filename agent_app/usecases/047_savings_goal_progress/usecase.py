"""Savings goal progress

Area: money
Reads the goal you saved and projects when you'll hit it.

Run:  python usecases/047_savings_goal_progress/usecase.py                  # your preferred framework
      python usecases/047_savings_goal_progress/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/047_savings_goal_progress/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=47,
    area="money",
    title="Savings goal progress",
    ask="How's the vacation fund coming along?",
    why="Reads the goal you saved and projects when you'll hit it.",
    tools=[T("goal_progress", "Progress on a savings goal.", {"goal": str}, {"target": 3000, "saved": 1950, "monthly": 350})],
    steps=[par(recall("vacation"), call("goal_progress", goal="vacation")),
           answer("$1,950 of $3,000. At $350 a month you'll get there in 3 months.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
