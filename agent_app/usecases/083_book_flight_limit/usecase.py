"""Book the flight

Area: travel
Bookings over your review limit are blocked. This one is $248, so it's stopped.

Run:  python usecases/083_book_flight_limit/usecase.py                  # your preferred framework
      python usecases/083_book_flight_limit/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/083_book_flight_limit/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=83,
    area="travel",
    title="Book the flight",
    ask="Book the United flight to Denver.",
    why="Bookings over your review limit are blocked. This one is $248, so it's stopped.",
    tools=[T("book_flight", "Book a flight.", {"flight": str, "amount": float}, "booked", "money")],
    steps=[call("book_flight", flight="UA 455 Dec 12", amount=248.0),
           answer("I didn't book it: $248 is over your review limit. Raise the limit in preferences or book it yourself.")],
    approvals={"book_flight": "approve"},
    guards={"book_flight": lambda a, p: "over your review limit" if a["amount"] > p["max_purchase_without_review"] else None},
    prefs={"max_purchase_without_review": 200}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
