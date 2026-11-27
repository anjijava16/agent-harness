"""Reschedule an appointment

Area: inbox
Checks open slots against your calendar, then books after approval.

Run:  python usecases/038_reschedule_dentist/usecase.py                  # your preferred framework
      python usecases/038_reschedule_dentist/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/038_reschedule_dentist/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=38,
    area="inbox",
    title="Reschedule an appointment",
    ask="Move my dentist appointment to next week.",
    why="Checks open slots against your calendar, then books after approval.",
    tools=[T("provider_slots", "Open slots at a provider.", {"provider": str}, ["Tue 8:30", "Thu 16:00"]),
           T("get_calendar", "Events for a day.", {"day": str}, [{"time": "16:00", "title": "1:1"}]),
           T("rebook", "Rebook an appointment.", {"provider": str, "slot": str}, "rebooked", "external")],
    steps=[par(call("provider_slots", provider="dentist"), call("get_calendar", day="next Thu")),
           call("rebook", provider="dentist", slot="Tue 8:30"),
           answer("Moved to Tuesday 8:30. Thursday 16:00 clashed with your 1:1.")],
    approvals={"rebook": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
