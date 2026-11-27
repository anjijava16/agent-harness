"""My year in review

Area: digital
Pulls from money, fitness, learning and memory for one look back at the year.

Run:  python usecases/200_year_in_review/usecase.py                  # your preferred framework
      python usecases/200_year_in_review/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/200_year_in_review/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=200,
    area="digital",
    title="My year in review",
    ask="Give me my year in review.",
    why="Pulls from money, fitness, learning and memory for one look back at the year.",
    tools=[T("totals", "Yearly totals.", {"kind": str}, lambda kind: {"saved": 9100, "km_run": 640, "books": 14}[kind])],
    steps=[par(call("totals", kind="saved"), call("totals", kind="km_run"), call("totals", kind="books"), recall("brag")),
           answer("2026: $9.1k saved, 640 km run, 14 books read, and you led the Q4 review across 4 teams.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
