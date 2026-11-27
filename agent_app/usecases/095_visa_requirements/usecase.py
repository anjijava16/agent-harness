"""Do I need a visa

Area: travel
Checks the current entry rules.

Run:  python usecases/095_visa_requirements/usecase.py                  # your preferred framework
      python usecases/095_visa_requirements/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/095_visa_requirements/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=95,
    area="travel",
    title="Do I need a visa",
    ask="Do I need a visa for a week in Japan?",
    why="Checks the current entry rules.",
    tools=[T("entry_rules", "Entry rules.", {"country": str, "citizenship": str}, {"visa_free_days": 90, "registration": "Visit Japan Web recommended"})],
    steps=[call("entry_rules", country="Japan", citizenship="US"),
           answer("No visa needed for up to 90 days. Fill in Visit Japan Web before you fly.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
