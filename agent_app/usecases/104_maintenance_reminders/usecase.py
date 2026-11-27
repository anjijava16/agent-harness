"""Home maintenance calendar

Area: home
Reads the maintenance log and schedules the next item.

Run:  python usecases/104_maintenance_reminders/usecase.py                  # your preferred framework
      python usecases/104_maintenance_reminders/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/104_maintenance_reminders/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=104,
    area="home",
    title="Home maintenance calendar",
    ask="What home maintenance is due?",
    why="Reads the maintenance log and schedules the next item.",
    tools=[T("maintenance_log", "Last time each task was done.", {"home": str}, {"furnace filter": "4 months ago", "smoke detectors": "11 months ago", "gutters": "2 months ago"}),
           T("add_event", "Add a calendar event.", {"title": str, "when": str}, "added", "write")],
    steps=[call("maintenance_log", home="main"),
           par(call("add_event", title="Replace furnace filter", when="Saturday"), call("add_event", title="Test smoke detectors", when="Saturday")),
           answer("The furnace filter (4 months) and the smoke detector test (11 months) are due. Both are on Saturday's calendar.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
