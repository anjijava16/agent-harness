"""How much is that in dollars

Area: money
Uses the live rate for your currency preference.

Run:  python usecases/053_currency_for_trip/usecase.py                  # your preferred framework
      python usecases/053_currency_for_trip/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/053_currency_for_trip/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=53,
    area="money",
    title="How much is that in dollars",
    ask="Convert 250 euros for my trip budget.",
    why="Uses the live rate for your currency preference.",
    tools=[T("fx_rate", "Exchange rate.", {"base": str, "quote": str}, 1.08)],
    steps=[call("fx_rate", base="EUR", quote="{currency}"), answer("250 EUR is about 270 {currency} at today's rate (1.08).")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
