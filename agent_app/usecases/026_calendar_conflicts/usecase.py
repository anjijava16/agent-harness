"""Calendar conflicts

Area: inbox
Checks work and family calendars together.

Run:  python usecases/026_calendar_conflicts/usecase.py                  # your preferred framework
      python usecases/026_calendar_conflicts/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/026_calendar_conflicts/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=26,
    area="inbox",
    title="Calendar conflicts",
    ask="Any double bookings this week?",
    why="Checks work and family calendars together.",
    tools=[T("events", "Events in a calendar.", {"calendar": str}, lambda calendar: {"work": [{"day": "Thu", "time": "17:00", "title": "Late review"}],
                                                                                   "family": [{"day": "Thu", "time": "17:00", "title": "Maya recital"}]}[calendar])],
    steps=[par(call("events", calendar="work"), call("events", calendar="family")),
           answer("One clash: Thursday 17:00, the late review overlaps {kid}'s recital. Move the review.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
