"""Turn a call into a walk

Area: health
Checks the weather and updates the event after approval.

Run:  python usecases/139_walking_meeting/usecase.py                  # your preferred framework
      python usecases/139_walking_meeting/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/139_walking_meeting/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=139,
    area="health",
    title="Turn a call into a walk",
    ask="Make my 3pm call a walking meeting if the weather's OK.",
    why="Checks the weather and updates the event after approval.",
    tools=[T("hourly_forecast", "Hourly forecast.", {"city": str}, {"15:00": "dry 47F"}),
           T("update_event", "Update an event.", {"title": str, "note": str}, "updated", "external")],
    steps=[call("hourly_forecast", city="{home_city}"), call("update_event", title="3pm call", note="Walking meeting, audio only"),
           answer("It'll be dry and 47F, so the 3pm call is now a walking meeting.")],
    approvals={"update_event": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
