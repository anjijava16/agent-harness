"""Save expiry dates

Area: digital
Only the dates are saved, never the ID numbers.

Run:  python usecases/186_save_expiry_dates/usecase.py                  # your preferred framework
      python usecases/186_save_expiry_dates/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/186_save_expiry_dates/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=186,
    area="digital",
    title="Save expiry dates",
    ask="My license expires March 2027, passport June 2027.",
    why="Only the dates are saved, never the ID numbers.",
    tools=[],
    steps=[remember("expiry", "license: 2027-03; passport: 2027-06"), remember("passport", "expires 2027-06"),
           answer("Saved the expiry dates.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
