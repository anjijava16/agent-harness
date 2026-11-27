"""File trip expenses

Area: travel
Collects receipts from email and submits the expense report after approval.

Run:  python usecases/089_expense_trip_receipts/usecase.py                  # your preferred framework
      python usecases/089_expense_trip_receipts/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/089_expense_trip_receipts/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=89,
    area="travel",
    title="File trip expenses",
    ask="File my Denver trip expenses.",
    why="Collects receipts from email and submits the expense report after approval.",
    tools=[T("search_receipts", "Search email receipts.", {"query": str}, [{"what": "hotel", "amount": 567}, {"what": "ride", "amount": 48}, {"what": "meals", "amount": 92}]),
           T("submit_expenses", "Submit an expense report.", {"trip": str, "total": float}, "submitted", "external")],
    steps=[call("search_receipts", query="Denver Dec"), call("submit_expenses", trip="Denver conference", total=707.0),
           answer("Expense report submitted: $707 (hotel $567, ride $48, meals $92).")],
    approvals={"submit_expenses": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
