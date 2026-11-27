"""Hobby spending

Area: learning
Totals by hobby.

Run:  python usecases/178_hobby_budget/usecase.py                  # your preferred framework
      python usecases/178_hobby_budget/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/178_hobby_budget/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=178,
    area="learning",
    title="Hobby spending",
    ask="How much did I spend on hobbies this year?",
    why="Totals by hobby.",
    tools=[T("spend_by_tag", "Spending by tag.", {"tag": str}, {"guitar": 340, "running": 410, "photography": 220})],
    steps=[call("spend_by_tag", tag="hobbies"), answer("$970 this year: running $410, guitar $340 and photography $220.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
