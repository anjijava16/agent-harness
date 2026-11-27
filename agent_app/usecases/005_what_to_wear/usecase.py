"""What should I wear

Area: mornings
Combines the forecast with what's on your calendar.

Run:  python usecases/005_what_to_wear/usecase.py                  # your preferred framework
      python usecases/005_what_to_wear/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/005_what_to_wear/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=5,
    area="mornings",
    title="What should I wear",
    ask="What should I wear today?",
    why="Combines the forecast with what's on your calendar.",
    tools=[T("hourly_forecast", "Hourly forecast.", {"city": str}, {"morning_f": 35, "afternoon_f": 44, "wind_mph": 18}),
           T("get_calendar", "Events for a day.", {"day": str}, [{"title": "Client lunch downtown"}])],
    steps=[par(call("hourly_forecast", city="{home_city}"), call("get_calendar", day="today")),
           answer("35F rising to 44 with 18 mph wind. You have a client lunch, so wear the wool coat over something smart, and a scarf.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
