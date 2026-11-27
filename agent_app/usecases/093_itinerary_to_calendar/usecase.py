"""Trip itinerary to calendar

Area: travel
Reads the confirmation emails and creates the events.

Run:  python usecases/093_itinerary_to_calendar/usecase.py                  # your preferred framework
      python usecases/093_itinerary_to_calendar/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/093_itinerary_to_calendar/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=93,
    area="travel",
    title="Trip itinerary to calendar",
    ask="Put my Denver itinerary on my calendar.",
    why="Reads the confirmation emails and creates the events.",
    tools=[T("trip_confirmations", "Booking confirmations.", {"trip": str}, [{"what": "Flight UA 455", "when": "Dec 12 07:10"}, {"what": "Maven hotel", "when": "Dec 12-15"}]),
           T("add_event", "Add a calendar event.", {"title": str, "when": str}, "added", "write")],
    steps=[call("trip_confirmations", trip="Denver"),
           par(call("add_event", title="Flight UA 455", when="Dec 12 07:10"), call("add_event", title="Maven hotel", when="Dec 12-15")),
           answer("Added the flight and the hotel stay to your calendar.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
