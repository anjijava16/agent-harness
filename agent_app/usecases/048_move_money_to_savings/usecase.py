"""Move money to savings

Area: money
Transfers need approval. You edit it down to $300 before it runs.

Run:  python usecases/048_move_money_to_savings/usecase.py                  # your preferred framework
      python usecases/048_move_money_to_savings/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/048_move_money_to_savings/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=48,
    area="money",
    title="Move money to savings",
    ask="Move $500 to savings.",
    why="Transfers need approval. You edit it down to $300 before it runs.",
    tools=[T("checking_balance", "Checking balance.", {"account": str}, {"balance": 2100}),
           T("transfer", "Transfer between your accounts.", {"amount": float, "to_account": str}, "transferred", "money")],
    steps=[call("checking_balance", account="checking"), call("transfer", amount=500.0, to_account="savings"),
           answer("Done. The transfer went through for the amount you set.")],
    approvals={"transfer": ("edit", {"amount": 300.0})},
    expect=[("$300 moved", lambda c: c["actions"][0]["args"]["amount"] == 300.0)]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
