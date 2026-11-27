"""Farmers market this weekend

Area: errands
Checks the market and the weather together.

Run:  python usecases/077_farmers_market/usecase.py                  # your preferred framework
      python usecases/077_farmers_market/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/077_farmers_market/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=77,
    area="errands",
    title="Farmers market this weekend",
    ask="What's at the farmers market this weekend?",
    why="Checks the market and the weather together.",
    tools=[T("market_info", "Farmers market info.", {"city": str}, {"day": "Sat", "hours": "8-13", "seasonal": ["squash", "apples"]}),
           T("get_weather", "Weather for a city.", {"city": str}, {"sat": "sunny 45F"})],
    steps=[par(call("market_info", city="{home_city}"), call("get_weather", city="{home_city}")),
           answer("Saturday 8 to 1, sunny and 45F. Squash and apples are in season.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
