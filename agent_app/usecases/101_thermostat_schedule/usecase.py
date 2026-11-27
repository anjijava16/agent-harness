"""Set the thermostat schedule

Area: home
Writes the schedule. Settings outside 55-75F are blocked.

Run:  python usecases/101_thermostat_schedule/usecase.py                  # your preferred framework
      python usecases/101_thermostat_schedule/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/101_thermostat_schedule/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=101,
    area="home",
    title="Set the thermostat schedule",
    ask="Set the heat to 68 when we're home, 60 at night.",
    why="Writes the schedule. Settings outside 55-75F are blocked.",
    tools=[T("set_schedule", "Set a thermostat schedule.", {"day_f": int, "night_f": int}, "set", "write")],
    steps=[call("set_schedule", day_f=68, night_f=60), answer("Schedule set: 68F during the day, 60F at night.")],
    guards={"set_schedule": lambda a, p: "outside the safe 55-75F range" if not (55 <= a["night_f"] <= 75 and 55 <= a["day_f"] <= 75) else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
