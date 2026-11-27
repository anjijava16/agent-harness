"""Book a haircut

Area: errands
Remembers your barber and preferred time, finds a slot, books after approval.

Run:  python usecases/066_book_haircut/usecase.py                  # your preferred framework
      python usecases/066_book_haircut/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/066_book_haircut/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=66,
    area="errands",
    title="Book a haircut",
    ask="Book my usual haircut next week.",
    why="Remembers your barber and preferred time, finds a slot, books after approval.",
    tools=[T("salon_slots", "Open slots.", {"salon": str}, ["Wed 18:00", "Sat 10:00"]),
           T("book", "Book a slot.", {"salon": str, "slot": str}, "booked", "external")],
    steps=[recall("haircut"), call("salon_slots", salon="Fade House"), call("book", salon="Fade House", slot="Sat 10:00"),
           answer("Booked at Fade House for Saturday 10:00.")],
    approvals={"book": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
