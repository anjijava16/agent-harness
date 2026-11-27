"""Start a return

Area: errands
Finds the order, checks the return window and starts the return after approval.

Run:  python usecases/064_return_an_item/usecase.py                  # your preferred framework
      python usecases/064_return_an_item/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/064_return_an_item/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=64,
    area="errands",
    title="Start a return",
    ask="Return the shoes that don't fit.",
    why="Finds the order, checks the return window and starts the return after approval.",
    tools=[T("find_order", "Find an order.", {"query": str}, {"order": "A-5512", "item": "Trail shoes", "days_since": 12, "window_days": 30}),
           T("start_return", "Start a return.", {"order": str, "reason": str}, {"label": "emailed", "dropoff": "UPS store"}, "external")],
    steps=[call("find_order", query="shoes"), call("start_return", order="A-5512", reason="doesn't fit"),
           answer("Return started for the trail shoes (day 12 of 30). The label is in your email; drop them at the UPS store.")],
    approvals={"start_return": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
