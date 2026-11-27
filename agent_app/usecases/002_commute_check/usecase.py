"""Commute check

Area: mornings
Checks transit alerts and traffic and picks the faster option.

Run:  python usecases/002_commute_check/usecase.py                  # your preferred framework
      python usecases/002_commute_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/002_commute_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=2,
    area="mornings",
    title="Commute check",
    ask="How's my commute looking?",
    why="Checks transit alerts and traffic and picks the faster option.",
    tools=[T("transit_alerts", "Transit alerts for a line.", {"line": str}, {"line": "Blue Line", "delay_min": 12, "reason": "signal problem"}),
           T("drive_time", "Driving time from home to work.", {"city": str}, {"minutes": 34})],
    steps=[par(call("transit_alerts", line="Blue Line"), call("drive_time", city="{home_city}")),
           answer("The Blue Line is running 12 minutes late (signal problem), about 40 minutes in total. Driving is 34. Drive today, or leave 15 minutes early for the train.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
