"""Why is the electric bill high

Area: home
Compares usage by device with last month.

Run:  python usecases/109_energy_usage/usecase.py                  # your preferred framework
      python usecases/109_energy_usage/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/109_energy_usage/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=109,
    area="home",
    title="Why is the electric bill high",
    ask="Why was the electric bill high this month?",
    why="Compares usage by device with last month.",
    tools=[T("usage_by_device", "Energy use by device.", {"month": str}, lambda month: {"this": {"space heater": 140, "dryer": 60}, "last": {"space heater": 20, "dryer": 55}}[month])],
    steps=[par(call("usage_by_device", month="this"), call("usage_by_device", month="last")),
           answer("The space heater went from 20 to 140 kWh. That's almost all of the increase.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
