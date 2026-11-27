"""Use the learning budget

Area: work
Checks the budget and enrolls. $349 is over your personal limit, but company-paid items have
their own check.

Run:  python usecases/151_learning_budget_course/usecase.py                  # your preferred framework
      python usecases/151_learning_budget_course/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/151_learning_budget_course/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=151,
    area="work",
    title="Use the learning budget",
    ask="Enroll me in the data analysis course with my learning budget.",
    why="Checks the budget and enrolls. $349 is over your personal limit, but company-paid items have their own check.",
    tools=[T("learning_budget", "Remaining learning budget.", {"year": int}, 1200),
           T("enroll", "Enroll in a course (company-paid).", {"course": str, "cost": float}, "enrolled", "money")],
    steps=[call("learning_budget", year=2026), call("enroll", course="Data Analysis with Python", cost=349.0),
           answer("You're enrolled in Data Analysis with Python ($349), with $851 of budget left.")],
    approvals={"enroll": "approve"},
    guards={"enroll": lambda a, p: "over remaining learning budget" if a["cost"] > 1200 else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
