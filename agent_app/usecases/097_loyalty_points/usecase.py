"""Points and miles check

Area: travel
Checks all programs at once.

Run:  python usecases/097_loyalty_points/usecase.py                  # your preferred framework
      python usecases/097_loyalty_points/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/097_loyalty_points/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=97,
    area="travel",
    title="Points and miles check",
    ask="How many points do I have, and are any expiring?",
    why="Checks all programs at once.",
    tools=[T("points", "Loyalty balance.", {"program": str}, lambda program: {"airline": {"balance": 42000, "expiring": 0}, "hotel": {"balance": 18000, "expiring": 18000, "on": "Jan 31"}}[program])],
    steps=[par(call("points", program="airline"), call("points", program="hotel")),
           answer("42k airline miles. Your 18k hotel points all expire Jan 31, so use them or earn something before then.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
