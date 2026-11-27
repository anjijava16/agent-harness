"""Split a dinner bill

Area: money
Calculates the split and sends payment requests after approval.

Run:  python usecases/045_split_dinner_bill/usecase.py                  # your preferred framework
      python usecases/045_split_dinner_bill/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/045_split_dinner_bill/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=45,
    area="money",
    title="Split a dinner bill",
    ask="Split last night's $186 dinner four ways and request payment.",
    why="Calculates the split and sends payment requests after approval.",
    tools=[T("request_payment", "Send a payment request.", {"to": str, "amount": float}, "requested", "money")],
    steps=[par(call("request_payment", to="Lee", amount=46.50), call("request_payment", to="Ana", amount=46.50), call("request_payment", to="Kai", amount=46.50)),
           answer("$46.50 each. Requests sent to Lee, Ana and Kai.")],
    approvals={"request_payment": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
