"""Bills due this week

Area: money
Reads every account in parallel and lists what's due and from where.

Run:  python usecases/041_bills_due_this_week/usecase.py                  # your preferred framework
      python usecases/041_bills_due_this_week/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/041_bills_due_this_week/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=41,
    area="money",
    title="Bills due this week",
    ask="What bills are due this week?",
    why="Reads every account in parallel and lists what's due and from where.",
    tools=[T("bills", "Upcoming bills for an account.", {"account": str}, lambda account: {"utilities": [{"name": "Electric", "due": "Wed", "amount": 84.10}],
                                                                                         "cards": [{"name": "Visa ending 4417", "due": "Fri", "amount": 512.00}]}[account])],
    steps=[par(call("bills", account="utilities"), call("bills", account="cards")),
           answer("Two bills: Electric $84.10 on Wednesday and the Visa ending 4417, $512.00, on Friday.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
