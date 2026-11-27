"""Compare insurance renewal quotes

Area: money
Gets quotes in parallel and compares them with the renewal.

Run:  python usecases/055_insurance_renewal_compare/usecase.py                  # your preferred framework
      python usecases/055_insurance_renewal_compare/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/055_insurance_renewal_compare/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=55,
    area="money",
    title="Compare insurance renewal quotes",
    ask="My car insurance renews next month. Is it a good price?",
    why="Gets quotes in parallel and compares them with the renewal.",
    tools=[T("renewal_quote", "Current insurer's renewal.", {"policy": str}, {"premium": 1480}),
           T("market_quote", "Quote from another insurer.", {"insurer": str}, lambda insurer: {"A": 1290, "B": 1550}[insurer])],
    steps=[par(call("renewal_quote", policy="auto"), call("market_quote", insurer="A"), call("market_quote", insurer="B")),
           answer("Renewal is $1,480. Insurer A quotes $1,290 for the same cover, so it's worth calling your insurer to match it.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
