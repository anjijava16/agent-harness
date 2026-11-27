"""Credit report alerts

Area: money
Reads monitoring alerts and points out anything unusual.

Run:  python usecases/052_credit_score_check/usecase.py                  # your preferred framework
      python usecases/052_credit_score_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/052_credit_score_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=52,
    area="money",
    title="Credit report alerts",
    ask="Any changes on my credit report?",
    why="Reads monitoring alerts and points out anything unusual.",
    tools=[T("credit_alerts", "Credit monitoring alerts.", {"days": int}, [{"type": "hard inquiry", "who": "AutoLoans Co", "date": "Nov 2"}])],
    steps=[call("credit_alerts", days=30),
           answer("One new hard inquiry from AutoLoans Co on Nov 2. If you didn't apply for a car loan, dispute it and freeze your credit.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
