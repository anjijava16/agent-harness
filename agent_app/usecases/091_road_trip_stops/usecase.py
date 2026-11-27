"""Road trip stops

Area: travel
Finds dog-friendly stops every two hours or so.

Run:  python usecases/091_road_trip_stops/usecase.py                  # your preferred framework
      python usecases/091_road_trip_stops/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/091_road_trip_stops/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=91,
    area="travel",
    title="Road trip stops",
    ask="Plan stops for the drive to Nashville with the dog.",
    why="Finds dog-friendly stops every two hours or so.",
    tools=[T("route_stops", "Stops along a route.", {"origin": str, "dest": str, "every_hours": int, "dog_friendly": bool},
             ["Indianapolis rest area (dog park)", "Louisville riverfront"])],
    steps=[call("route_stops", origin="{home_city}", dest="Nashville", every_hours=2, dog_friendly=True),
           answer("Stop at the Indianapolis rest area (it has a dog park) and the Louisville riverfront. {dog} will be happy.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
