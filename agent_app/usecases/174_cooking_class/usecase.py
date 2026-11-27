"""Book a cooking class

Area: learning
Booking for two, with approval.

Run:  python usecases/174_cooking_class/usecase.py                  # your preferred framework
      python usecases/174_cooking_class/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/174_cooking_class/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=174,
    area="learning",
    title="Book a cooking class",
    ask="Book a pasta-making class for Jordan and me.",
    why="Booking for two, with approval.",
    tools=[T("classes", "Classes.", {"day": str, "kind": str}, [{"class": "Fresh pasta", "time": "Sat 15:00", "price": 85}]),
           T("book_class", "Book a class.", {"class_name": str, "time": str}, "booked", "external")],
    steps=[call("classes", day="Sat", kind="cooking"), call("book_class", class_name="Fresh pasta", time="Sat 15:00"),
           answer("Fresh pasta class booked for you and {partner}, Saturday at 15:00.")],
    approvals={"book_class": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
