"""Plan my day from my task list

Area: mornings
Fits open tasks into calendar gaps inside your work hours, and saves the plan.

Run:  python usecases/003_day_plan_from_tasks/usecase.py                  # your preferred framework
      python usecases/003_day_plan_from_tasks/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/003_day_plan_from_tasks/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=3,
    area="mornings",
    title="Plan my day from my task list",
    ask="Plan my day around my meetings.",
    why="Fits open tasks into calendar gaps inside your work hours, and saves the plan.",
    tools=[T("get_calendar", "Events for a day.", {"day": str}, [{"time": "09:30-10:00", "title": "Standup"}, {"time": "14:00-15:00", "title": "1:1"}]),
           T("open_tasks", "Open tasks with estimates.", {"list": str}, [{"task": "Quarterly report draft", "mins": 90}, {"task": "Expense report", "mins": 20}, {"task": "Call plumber", "mins": 10}])],
    steps=[par(call("get_calendar", day="today"), call("open_tasks", list="today")),
           remember("plan_today", "10:00 report draft, 11:30 expenses, 12:00 call plumber"),
           answer("Plan inside {work_hours}: report draft 10:00-11:30, expenses 11:30, plumber at 12:00. The afternoon is free after your 1:1.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
