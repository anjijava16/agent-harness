"""Monthly learning review

Area: learning
Course, language and practice data in one review.

Run:  python usecases/180_monthly_learning_review/usecase.py                  # your preferred framework
      python usecases/180_monthly_learning_review/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/180_monthly_learning_review/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=180,
    area="learning",
    title="Monthly learning review",
    ask="What did I learn this month?",
    why="Course, language and practice data in one review.",
    tools=[T("course_progress", "Course progress.", {"course": str}, {"done": 13, "total": 24}),
           T("practice_month", "Practice minutes this month.", {"instrument": str}, 380)],
    steps=[par(call("course_progress", course="Data Analysis with Python"), call("practice_month", instrument="guitar"), recall("spanish")),
           answer("13 of 24 course lessons done, 380 minutes of guitar, and Spanish is at A2 (preterite).")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
