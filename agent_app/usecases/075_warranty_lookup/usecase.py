"""Is it still under warranty

Area: errands
Finds the purchase receipt and the warranty terms.

Run:  python usecases/075_warranty_lookup/usecase.py                  # your preferred framework
      python usecases/075_warranty_lookup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/075_warranty_lookup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=75,
    area="errands",
    title="Is it still under warranty",
    ask="Is the dishwasher still under warranty?",
    why="Finds the purchase receipt and the warranty terms.",
    tools=[T("search_receipts", "Search email receipts.", {"query": str}, [{"item": "Dishwasher", "bought": "2025-03-10"}]),
           T("warranty_terms", "Warranty terms for a product.", {"item": str}, {"years": 2})],
    steps=[call("search_receipts", query="dishwasher"), call("warranty_terms", item="Dishwasher"),
           answer("Yes, until March 2027 (2 years from March 10, 2025).")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
