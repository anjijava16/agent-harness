"""Price drop after I bought it

Area: money
Checks recent orders against current prices and files a price-adjustment request after approval.

Run:  python usecases/050_price_drop_refund/usecase.py                  # your preferred framework
      python usecases/050_price_drop_refund/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/050_price_drop_refund/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=50,
    area="money",
    title="Price drop after I bought it",
    ask="Did anything I bought recently drop in price?",
    why="Checks recent orders against current prices and files a price-adjustment request after approval.",
    tools=[T("recent_orders", "Recent orders.", {"days": int}, [{"item": "Air fryer", "paid": 129.0, "store": "HomeMart"}]),
           T("current_price", "Current price of an item.", {"item": str}, 99.0),
           T("request_price_adjustment", "Ask a store for a price adjustment.", {"item": str, "refund": float}, "submitted", "external")],
    steps=[call("recent_orders", days=14), call("current_price", item="Air fryer"),
           call("request_price_adjustment", item="Air fryer", refund=30.0),
           answer("The air fryer dropped from $129 to $99. A $30 price-adjustment request has gone to HomeMart.")],
    approvals={"request_price_adjustment": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
