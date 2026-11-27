"""Monthly budget review

Area: money
Compares spending by category with the budget you set.

Run:  python usecases/043_monthly_budget_review/usecase.py                  # your preferred framework
      python usecases/043_monthly_budget_review/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/043_monthly_budget_review/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=43,
    area="money",
    title="Monthly budget review",
    ask="How did I do against my budget this month?",
    why="Compares spending by category with the budget you set.",
    tools=[T("spending_by_category", "Spending this month.", {"month": str}, {"groceries": 640, "dining": 310, "transport": 120}),
           T("budget", "Your budget.", {"month": str}, {"groceries": 600, "dining": 250, "transport": 200})],
    steps=[par(call("spending_by_category", month="this"), call("budget", month="this")),
           answer("Over on groceries ($640 vs $600) and dining ($310 vs $250). Transport is $80 under.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
