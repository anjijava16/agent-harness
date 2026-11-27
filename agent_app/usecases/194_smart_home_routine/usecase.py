"""Leaving-home routine

Area: digital
Lights off, thermostat down, and the cameras on.

Run:  python usecases/194_smart_home_routine/usecase.py                  # your preferred framework
      python usecases/194_smart_home_routine/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/194_smart_home_routine/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=194,
    area="digital",
    title="Leaving-home routine",
    ask="Run my leaving-home routine.",
    why="Lights off, thermostat down, and the cameras on.",
    tools=[T("set_lights", "Set lights.", {"room": str, "level": int}, "ok", "write"),
           T("set_thermostat", "Set the thermostat.", {"temp_f": int}, "set", "write"),
           T("cameras", "Turn cameras on or off.", {"on": bool}, "on", "write")],
    steps=[par(call("set_lights", room="all", level=0), call("set_thermostat", temp_f=62), call("cameras", on=True)),
           answer("Lights off, heat at 62F, cameras on.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
