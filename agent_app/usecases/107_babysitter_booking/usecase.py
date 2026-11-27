"""Book a babysitter

Area: home
Asks your saved sitters. Booking is a payment, so it needs approval.

Run:  python usecases/107_babysitter_booking/usecase.py                  # your preferred framework
      python usecases/107_babysitter_booking/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/107_babysitter_booking/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=107,
    area="home",
    title="Book a babysitter",
    ask="Book a sitter for Saturday 6-11pm.",
    why="Asks your saved sitters. Booking is a payment, so it needs approval.",
    tools=[T("ask_sitters", "Check sitters' availability.", {"date": str, "hours": str}, [{"name": "Emma", "available": True, "rate": 20}]),
           T("book_sitter", "Book a sitter.", {"name": str, "hours": int, "rate": float}, "booked", "money")],
    steps=[call("ask_sitters", date="Sat", hours="18-23"), call("book_sitter", name="Emma", hours=5, rate=20.0),
           answer("Emma is booked for Saturday 6-11pm ($100).")],
    approvals={"book_sitter": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
