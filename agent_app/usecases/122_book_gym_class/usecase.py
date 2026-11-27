"""Book a gym class

Area: health
Finds a class and books after approval.

Run:  python usecases/122_book_gym_class/usecase.py                  # your preferred framework
      python usecases/122_book_gym_class/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/122_book_gym_class/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=122,
    area="health",
    title="Book a gym class",
    ask="Book a spin class for Wednesday evening.",
    why="Finds a class and books after approval.",
    tools=[T("classes", "Gym classes.", {"day": str, "kind": str}, [{"class": "Spin", "time": "18:15", "spots": 4}]),
           T("book_class", "Book a class.", {"class_name": str, "time": str}, "booked", "external")],
    steps=[call("classes", day="Wed", kind="spin"), call("book_class", class_name="Spin", time="18:15"),
           answer("Spin is booked for Wednesday 18:15 (4 spots were left).")],
    approvals={"book_class": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
