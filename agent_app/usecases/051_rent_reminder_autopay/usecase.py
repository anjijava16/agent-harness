"""Set up rent autopay

Area: money
Creating recurring payments needs approval. Amounts over $3,000 are blocked.

Run:  python usecases/051_rent_reminder_autopay/usecase.py                  # your preferred framework
      python usecases/051_rent_reminder_autopay/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/051_rent_reminder_autopay/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=51,
    area="money",
    title="Set up rent autopay",
    ask="Set up rent autopay for the 1st.",
    why="Creating recurring payments needs approval. Amounts over $3,000 are blocked.",
    tools=[T("create_autopay", "Create a recurring payment.", {"payee": str, "amount": float, "day": int}, "created", "money")],
    steps=[call("create_autopay", payee="Landlord", amount=2150.0, day=1),
           answer("Autopay set: $2,150 to your landlord on the 1st of each month.")],
    approvals={"create_autopay": "approve"},
    guards={"create_autopay": lambda a, p: "recurring payments over 3000 need the bank app" if a["amount"] > 3000 else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
