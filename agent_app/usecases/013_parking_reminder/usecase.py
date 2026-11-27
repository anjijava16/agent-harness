"""Street cleaning check

Area: mornings
Checks the city street-cleaning schedule for your block.

Run:  python usecases/013_parking_reminder/usecase.py                  # your preferred framework
      python usecases/013_parking_reminder/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/013_parking_reminder/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=13,
    area="mornings",
    title="Street cleaning check",
    ask="Do I need to move my car today?",
    why="Checks the city street-cleaning schedule for your block.",
    tools=[T("street_cleaning", "Street cleaning for an address.", {"city": str, "block": str}, {"today": True, "window": "9am-2pm"})],
    steps=[recall("parking"), call("street_cleaning", city="{home_city}", block="2100 N Damen"),
           answer("Yes: street cleaning on your block from 9 to 2. Move the car before 9.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
