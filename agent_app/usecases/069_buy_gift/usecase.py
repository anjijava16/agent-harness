"""Buy and ship a gift

Area: errands
Within your limit, so it only needs your approval.

Run:  python usecases/069_buy_gift/usecase.py                  # your preferred framework
      python usecases/069_buy_gift/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/069_buy_gift/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=69,
    area="errands",
    title="Buy and ship a gift",
    ask="Order the trail running vest, gift wrapped.",
    why="Within your limit, so it only needs your approval.",
    tools=[T("checkout", "Place the order.", {"item": str, "amount": float, "gift_wrap": bool}, "ordered", "money")],
    steps=[call("checkout", item="Trail running vest", amount=75.0, gift_wrap=True),
           answer("Ordered, gift wrapped, $75.")],
    approvals={"checkout": "approve"},
    guards={"checkout": lambda a, p: f"over your {p['currency']} {p['max_purchase_without_review']} limit" if a["amount"] > p["max_purchase_without_review"] else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
