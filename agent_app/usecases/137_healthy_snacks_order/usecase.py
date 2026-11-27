"""Order healthy snacks for the office

Area: health
Small purchase, within your limit, with approval.

Run:  python usecases/137_healthy_snacks_order/usecase.py                  # your preferred framework
      python usecases/137_healthy_snacks_order/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/137_healthy_snacks_order/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=137,
    area="health",
    title="Order healthy snacks for the office",
    ask="Order snacks for my desk.",
    why="Small purchase, within your limit, with approval.",
    tools=[T("checkout", "Place an order.", {"item": str, "amount": float}, "ordered", "money")],
    steps=[call("checkout", item="nuts and dried fruit variety box", amount=32.0), answer("Ordered a $32 snack box for your desk.")],
    approvals={"checkout": "approve"},
    guards={"checkout": lambda a, p: "over your review limit" if a["amount"] > p["max_purchase_without_review"] else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
