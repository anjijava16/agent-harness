"""Draft my standup update

Area: work
Built from yesterday's finished tasks and today's plan.

Run:  python usecases/141_standup_update/usecase.py                  # your preferred framework
      python usecases/141_standup_update/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/141_standup_update/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=141,
    area="work",
    title="Draft my standup update",
    ask="Draft my standup update.",
    why="Built from yesterday's finished tasks and today's plan.",
    tools=[T("done_tasks", "Tasks done.", {"day": str}, ["Report draft", "Expense report"]),
           T("open_tasks", "Open tasks.", {"list": str}, [{"task": "Vendor quotes"}])],
    steps=[par(call("done_tasks", day="yesterday"), call("open_tasks", list="today"), recall("plan_today")),
           answer("Yesterday: report draft and expenses. Today: vendor quotes. No blockers.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
