"""Kid allowance

Area: home
A small transfer to the kid's account after approval.

Run:  python usecases/118_allowance_tracker/usecase.py                  # your preferred framework
      python usecases/118_allowance_tracker/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/118_allowance_tracker/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=118,
    area="home",
    title="Kid allowance",
    ask="Pay Maya's weekly allowance.",
    why="A small transfer to the kid's account after approval.",
    tools=[T("transfer_to_kid", "Transfer to the kid's account.", {"kid_name": str, "amount": float}, "sent", "money")],
    steps=[call("transfer_to_kid", kid_name="{kid}", amount=10.0), answer("$10 allowance sent to {kid}.")],
    approvals={"transfer_to_kid": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
