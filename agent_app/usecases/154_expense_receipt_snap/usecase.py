"""Submit a lunch receipt

Area: work
Reads the receipt and submits after approval. Claims over $150 are blocked.

Run:  python usecases/154_expense_receipt_snap/usecase.py                  # your preferred framework
      python usecases/154_expense_receipt_snap/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/154_expense_receipt_snap/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=154,
    area="work",
    title="Submit a lunch receipt",
    ask="Submit yesterday's client lunch receipt.",
    why="Reads the receipt and submits after approval. Claims over $150 are blocked.",
    tools=[T("receipt_scan", "Read a receipt photo.", {"photo": str}, {"merchant": "Bistro 110", "amount": 86.40}),
           T("submit_expense", "Submit an expense.", {"merchant": str, "amount": float, "category": str}, "submitted", "external")],
    steps=[call("receipt_scan", photo="latest"), call("submit_expense", merchant="Bistro 110", amount=86.40, category="client meals"),
           answer("Submitted: Bistro 110, $86.40, client meals.")],
    approvals={"submit_expense": "approve"},
    guards={"submit_expense": lambda a, p: "meal claims over 150 need a manager" if a["amount"] > 150 else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
