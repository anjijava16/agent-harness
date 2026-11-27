"""Concert tickets

Area: learning
A purchase with approval, inside your limit.

Run:  python usecases/169_buy_concert_tickets/usecase.py                  # your preferred framework
      python usecases/169_buy_concert_tickets/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/169_buy_concert_tickets/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=169,
    area="learning",
    title="Concert tickets",
    ask="Get 2 tickets for the jazz show Friday.",
    why="A purchase with approval, inside your limit.",
    tools=[T("ticket_price", "Ticket price.", {"event": str, "qty": int}, 76.0),
           T("buy_tickets", "Buy tickets.", {"event": str, "qty": int, "amount": float}, "bought", "money")],
    steps=[call("ticket_price", event="Jazz at Green Mill", qty=2), call("buy_tickets", event="Jazz at Green Mill", qty=2, amount=76.0),
           answer("Two tickets for Friday's jazz show, $76 total.")],
    approvals={"buy_tickets": "approve"},
    guards={"buy_tickets": lambda a, p: "over your review limit" if a["amount"] > p["max_purchase_without_review"] else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
