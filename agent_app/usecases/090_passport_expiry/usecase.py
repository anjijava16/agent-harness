"""Passport expiry check

Area: travel
Checks the expiry date you saved against the entry rules.

Run:  python usecases/090_passport_expiry/usecase.py                  # your preferred framework
      python usecases/090_passport_expiry/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/090_passport_expiry/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=90,
    area="travel",
    title="Passport expiry check",
    ask="Is my passport OK for Spain next spring?",
    why="Checks the expiry date you saved against the entry rules.",
    tools=[T("entry_rules", "Entry rules for a country.", {"country": str}, {"passport_valid_months_after": 3})],
    steps=[par(recall("passport"), call("entry_rules", country="Spain")),
           answer("Your passport expires June 2027. Spain needs 3 months beyond your stay, so a spring trip is fine.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
