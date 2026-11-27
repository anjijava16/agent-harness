"""Photo spots at sunset

Area: learning
Sunset times and spots, with the weather check.

Run:  python usecases/170_photography_tips/usecase.py                  # your preferred framework
      python usecases/170_photography_tips/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/170_photography_tips/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=170,
    area="learning",
    title="Photo spots at sunset",
    ask="Where should I take sunset photos this week?",
    why="Sunset times and spots, with the weather check.",
    tools=[T("sunset", "Sunset time.", {"city": str}, "16:22"),
           T("photo_spots", "Photo spots.", {"city": str}, ["North Avenue Beach", "Montrose Harbor"]),
           T("get_weather", "Weather.", {"city": str}, {"clear_days": ["Wed", "Thu"]})],
    steps=[par(call("sunset", city="{home_city}"), call("photo_spots", city="{home_city}"), call("get_weather", city="{home_city}")),
           answer("Go Wednesday or Thursday (both clear). Sunset is at 16:22; Montrose Harbor and North Avenue Beach are both good spots.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
