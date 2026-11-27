"""Collect donation receipts

Area: money
Searches email, totals the amounts and saves the list for tax time.

Run:  python usecases/054_donation_receipts/usecase.py                  # your preferred framework
      python usecases/054_donation_receipts/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/054_donation_receipts/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=54,
    area="money",
    title="Collect donation receipts",
    ask="Gather my donation receipts for the year.",
    why="Searches email, totals the amounts and saves the list for tax time.",
    tools=[T("search_receipts", "Search email receipts.", {"query": str}, [{"org": "Food Depository", "amount": 150}, {"org": "Public Radio", "amount": 120}])],
    steps=[call("search_receipts", query="donation receipt 2026"), remember("tax_donations_2026", "Food Depository 150; Public Radio 120; total 270"),
           answer("$270 total across 2 organizations. Saved for tax time.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
