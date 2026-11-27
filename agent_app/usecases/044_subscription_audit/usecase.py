"""Subscription audit

Area: money
Finds recurring charges and cancels one after approval.

Run:  python usecases/044_subscription_audit/usecase.py                  # your preferred framework
      python usecases/044_subscription_audit/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/044_subscription_audit/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=44,
    area="money",
    title="Subscription audit",
    ask="What subscriptions am I paying for?",
    why="Finds recurring charges and cancels one after approval.",
    tools=[T("recurring_charges", "Recurring charges.", {"months": int}, [{"name": "StreamPlus", "amount": 15.99, "last_used_days": 70}, {"name": "Cloud storage", "amount": 2.99, "last_used_days": 1}]),
           T("cancel_subscription", "Cancel a subscription.", {"name": str}, "cancelled", "external")],
    steps=[call("recurring_charges", months=3), call("cancel_subscription", name="StreamPlus"),
           answer("Two subscriptions. You cancelled StreamPlus ($15.99/mo, unused for 70 days), saving $192 a year.")],
    approvals={"cancel_subscription": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
