"""Buy a new laptop

Area: money
An example of the guard: the agent tries, and your limit stops it.

Run:  python usecases/056_big_purchase_blocked/usecase.py                  # your preferred framework
      python usecases/056_big_purchase_blocked/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/056_big_purchase_blocked/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=56,
    area="money",
    title="Buy a new laptop",
    ask="Buy the laptop in my cart.",
    why="An example of the guard: the agent tries, and your limit stops it.",
    tools=[T("cart_total", "Cart total.", {"store": str}, {"items": ["Laptop 14-inch"], "amount": 1299.0}),
           T("checkout", "Place the order.", {"store": str, "amount": float}, "ordered", "money")],
    steps=[call("cart_total", store="TechStore"), call("checkout", store="TechStore", amount=1299.0),
           answer("I didn't buy it. $1,299 is over your review limit; check out yourself when you're ready.")],
    approvals={"checkout": "approve"},
    guards={"checkout": lambda a, p: f"over your {p['currency']} {p['max_purchase_without_review']} limit" if a["amount"] > p["max_purchase_without_review"] else None},
    expect=[("nothing bought", lambda c: not c["actions"])]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
