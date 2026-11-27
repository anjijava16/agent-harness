"""Weekend trip ideas

Area: travel
Checks drive times and weekend weather for a few places in parallel.

Run:  python usecases/081_weekend_trip_ideas/usecase.py                  # your preferred framework
      python usecases/081_weekend_trip_ideas/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/081_weekend_trip_ideas/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=81,
    area="travel",
    title="Weekend trip ideas",
    ask="Ideas for a weekend away within 4 hours' drive?",
    why="Checks drive times and weekend weather for a few places in parallel.",
    tools=[T("drive_time_to", "Drive time from your city.", {"origin": str, "dest": str}, lambda origin, dest: {"Door County": 4.0, "Galena": 2.8, "Milwaukee": 1.5}[dest]),
           T("weekend_weather", "Weekend forecast.", {"place": str}, lambda place: {"Door County": "snow", "Galena": "clear 40F", "Milwaukee": "rain"}[place])],
    steps=[par(call("drive_time_to", origin="{home_city}", dest="Galena"), call("drive_time_to", origin="{home_city}", dest="Door County"), call("drive_time_to", origin="{home_city}", dest="Milwaukee")),
           par(call("weekend_weather", place="Galena"), call("weekend_weather", place="Door County")),
           answer("Galena: 2.8 hours away and clear at 40F. Door County is at the 4-hour limit and getting snow.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
