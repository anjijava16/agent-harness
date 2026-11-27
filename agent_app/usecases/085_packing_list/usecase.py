"""Packing list

Area: travel
Uses the forecast, the trip length and your saved packing basics.

Run:  python usecases/085_packing_list/usecase.py                  # your preferred framework
      python usecases/085_packing_list/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/085_packing_list/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=85,
    area="travel",
    title="Packing list",
    ask="Make a packing list for Denver.",
    why="Uses the forecast, the trip length and your saved packing basics.",
    tools=[T("trip_forecast", "Forecast for trip dates.", {"city": str, "dates": str}, {"highs_f": [38, 45, 41], "snow": "Sat"})],
    steps=[par(call("trip_forecast", city="Denver", dates="Dec 12-15"), recall("packing")),
           answer("3 nights, highs 38-45F, snow Saturday. Pack layers, boots, a warm jacket, the laptop charger and your usual basics.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
