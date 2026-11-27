"""Check an unusual charge

Area: money
Matches the charge against your calendar and email receipts.

Run:  python usecases/046_unusual_charge_check/usecase.py                  # your preferred framework
      python usecases/046_unusual_charge_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/046_unusual_charge_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=46,
    area="money",
    title="Check an unusual charge",
    ask="What's this $89 charge from 'SQ *BLUEDOOR'?",
    why="Matches the charge against your calendar and email receipts.",
    tools=[T("find_transaction", "Find a card transaction.", {"merchant": str}, {"date": "Sat", "amount": 89.0, "city": "Chicago"}),
           T("search_receipts", "Search email receipts.", {"query": str}, ["Blue Door Kitchen, Sat, $89.00"])],
    steps=[call("find_transaction", merchant="BLUEDOOR"), call("search_receipts", query="Blue Door"),
           answer("It's Blue Door Kitchen, Saturday's dinner. The receipt in your email matches, so the charge is legitimate.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
