"""Order groceries for delivery

Area: errands
Builds the cart and checks it against your monthly grocery budget before ordering.

Run:  python usecases/062_order_groceries/usecase.py                  # your preferred framework
      python usecases/062_order_groceries/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/062_order_groceries/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=62,
    area="errands",
    title="Order groceries for delivery",
    ask="Order my grocery list for Saturday morning delivery.",
    why="Builds the cart and checks it against your monthly grocery budget before ordering.",
    tools=[T("build_cart", "Build a grocery cart.", {"items": str}, {"total": 64.20}),
           T("month_grocery_spend", "Grocery spending so far this month.", {"month": str}, 480.0),
           T("place_grocery_order", "Place a grocery order.", {"amount": float, "slot": str}, "ordered", "money")],
    steps=[par(recall("grocery_list"), call("month_grocery_spend", month="this")), call("build_cart", items="from list"),
           call("place_grocery_order", amount=64.20, slot="Sat 9-11"),
           answer("Ordered: $64.20, delivered Saturday 9-11. That brings you to $544 of your $600 grocery budget.")],
    approvals={"place_grocery_order": "approve"},
    guards={"place_grocery_order": lambda a, p: "over the monthly grocery budget" if 480 + a["amount"] > p["monthly_grocery_budget"] else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
