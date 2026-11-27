"""Year-end money summary

Area: money
Income, spending and savings in parallel, as a short report.

Run:  python usecases/060_year_end_money_summary/usecase.py                  # your preferred framework
      python usecases/060_year_end_money_summary/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/060_year_end_money_summary/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=60,
    area="money",
    title="Year-end money summary",
    ask="Give me my money summary for the year.",
    why="Income, spending and savings in parallel, as a short report.",
    tools=[T("totals", "Yearly totals.", {"kind": str}, lambda kind: {"spending": 48200, "saved": 9100}[kind]),
           T("top_categories", "Top spending categories.", {"year": int}, ["rent", "groceries", "travel"])],
    steps=[par(call("totals", kind="spending"), call("totals", kind="saved"), call("top_categories", year=2026)),
           answer("2026: $48.2k spent and $9.1k saved. The biggest costs were rent, groceries and travel.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
