"""Online course progress

Area: learning
Reads progress and suggests a pace to finish on time.

Run:  python usecases/164_course_progress/usecase.py                  # your preferred framework
      python usecases/164_course_progress/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/164_course_progress/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=164,
    area="learning",
    title="Online course progress",
    ask="How far am I in the data analysis course?",
    why="Reads progress and suggests a pace to finish on time.",
    tools=[T("course_progress", "Course progress.", {"course": str}, {"done": 9, "total": 24, "deadline": "Jan 31"})],
    steps=[call("course_progress", course="Data Analysis with Python"),
           answer("9 of 24 lessons done. Do 2 a week to finish by Jan 31.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
