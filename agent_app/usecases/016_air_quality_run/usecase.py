"""Is it OK to run outside

Area: mornings
Air quality and weather together, plus your saved running preferences.

Run:  python usecases/016_air_quality_run/usecase.py                  # your preferred framework
      python usecases/016_air_quality_run/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/016_air_quality_run/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=16,
    area="mornings",
    title="Is it OK to run outside",
    ask="Can I run outside this morning?",
    why="Air quality and weather together, plus your saved running preferences.",
    tools=[T("air_quality", "AQI for a city.", {"city": str}, {"aqi": 38, "label": "good"}),
           T("get_weather", "Weather for a city.", {"city": str}, {"temp_f": 36, "wind_mph": 10})],
    steps=[par(call("air_quality", city="{home_city}"), call("get_weather", city="{home_city}"), recall("running")),
           answer("Yes. Air quality is good (AQI 38), it's 36F with light wind. Gloves on.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
