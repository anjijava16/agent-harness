"""Household expenses with Jordan

Area: money
Totals the shared expense log and settles up after approval.

Run:  python usecases/059_shared_expenses/usecase.py                  # your preferred framework
      python usecases/059_shared_expenses/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/059_shared_expenses/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=59,
    area="money",
    title="Household expenses with Jordan",
    ask="What do Jordan and I owe each other this month?",
    why="Totals the shared expense log and settles up after approval.",
    tools=[T("shared_expenses", "Shared expenses.", {"with_person": str}, {"sam_paid": 820, "partner_paid": 560}),
           T("request_payment", "Send a payment request.", {"to": str, "amount": float}, "requested", "money")],
    steps=[call("shared_expenses", with_person="{partner}"), call("request_payment", to="{partner}", amount=130.0),
           answer("You paid $820 and {partner} paid $560, so {partner} owes you $130. The request is sent.")],
    approvals={"request_payment": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
