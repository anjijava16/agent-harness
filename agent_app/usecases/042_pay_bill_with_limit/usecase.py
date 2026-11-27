"""Pay a bill (with a spending limit)

Area: money
Payments need approval, and anything over your max_purchase_without_review preference is blocked
in code.

Run:  python usecases/042_pay_bill_with_limit/usecase.py                  # your preferred framework
      python usecases/042_pay_bill_with_limit/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/042_pay_bill_with_limit/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=42,
    area="money",
    title="Pay a bill (with a spending limit)",
    ask="Pay the electric bill and the Visa.",
    why="Payments need approval, and anything over your max_purchase_without_review preference is blocked in code.",
    tools=[T("pay_bill", "Pay a bill.", {"payee": str, "amount": float}, "paid", "money")],
    steps=[par(call("pay_bill", payee="Electric", amount=84.10), call("pay_bill", payee="Visa ending 4417", amount=512.00)),
           answer("Electric is paid ($84.10). The Visa payment ($512) is over your review limit, so pay it yourself in the bank app.")],
    approvals={"pay_bill": "approve"},
    guards={"pay_bill": lambda a, p: f"over your {p['currency']} {p['max_purchase_without_review']} limit" if a["amount"] > p["max_purchase_without_review"] else None},
    expect=[("only the small bill paid", lambda c: [a["args"]["payee"] for a in c["actions"]] == ["Electric"])]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
