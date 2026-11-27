"""Cheaper commute

Area: travel
Compares what you spend on commuting with a bike-share plan.

Run:  python usecases/098_commute_alternatives/usecase.py                  # your preferred framework
      python usecases/098_commute_alternatives/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/098_commute_alternatives/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=98,
    area="travel",
    title="Cheaper commute",
    ask="Would biking to work save me money?",
    why="Compares what you spend on commuting with a bike-share plan.",
    tools=[T("commute_spend", "Monthly commute spending.", {"months": int}, 132.0),
           T("bike_share_price", "Bike share annual plan.", {"city": str}, 143.0)],
    steps=[par(call("commute_spend", months=3), call("bike_share_price", city="{home_city}")),
           answer("You spend about $132 a month commuting. The bike share is $143 a year, so biking on dry days would save a lot.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
