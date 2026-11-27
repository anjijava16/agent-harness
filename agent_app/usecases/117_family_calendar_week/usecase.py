"""Family week overview

Area: home
Merges three calendars into one view.

Run:  python usecases/117_family_calendar_week/usecase.py                  # your preferred framework
      python usecases/117_family_calendar_week/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/117_family_calendar_week/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=117,
    area="home",
    title="Family week overview",
    ask="What's the family doing this week?",
    why="Merges three calendars into one view.",
    tools=[T("events", "Events in a calendar.", {"calendar": str}, lambda calendar: {"sam": ["Wed late meeting"], "partner": ["Tue gym 6pm"], "kid": ["Thu recital", "Sat swim"]}[calendar])],
    steps=[par(call("events", calendar="sam"), call("events", calendar="partner"), call("events", calendar="kid")),
           answer("Tue: {partner} at the gym at 6. Wed: your late meeting. Thu: {kid}'s recital. Sat: swim.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
