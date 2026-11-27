"""Hire help for a task

Area: errands
Compares task-helper quotes and books after approval.

Run:  python usecases/076_furniture_assembly/usecase.py                  # your preferred framework
      python usecases/076_furniture_assembly/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/076_furniture_assembly/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=76,
    area="errands",
    title="Hire help for a task",
    ask="Find someone to assemble a bookshelf this weekend.",
    why="Compares task-helper quotes and books after approval.",
    tools=[T("helper_quotes", "Quotes for a task.", {"task": str}, [{"name": "Ray", "price": 60, "rating": 4.9}, {"name": "Lou", "price": 45, "rating": 4.2}]),
           T("hire", "Hire a helper.", {"name": str, "price": float}, "booked", "money")],
    steps=[call("helper_quotes", task="assemble bookshelf"), call("hire", name="Ray", price=60.0),
           answer("Ray is booked for $60 (rated 4.9) this weekend.")],
    approvals={"hire": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
