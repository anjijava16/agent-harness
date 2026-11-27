"""Set a dining spending alert

Area: money
Creates a bank alert and remembers the threshold for the budget review.

Run:  python usecases/058_set_spending_alert/usecase.py                  # your preferred framework
      python usecases/058_set_spending_alert/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/058_set_spending_alert/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=58,
    area="money",
    title="Set a dining spending alert",
    ask="Alert me if dining goes over $250 this month.",
    why="Creates a bank alert and remembers the threshold for the budget review.",
    tools=[T("create_alert", "Create a spending alert.", {"category": str, "threshold": float}, "created", "write")],
    steps=[call("create_alert", category="dining", threshold=250.0), remember("dining_limit", "250"),
           answer("Alert set: you'll hear from your bank if dining goes over $250 this month.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
