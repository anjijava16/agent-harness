"""What's open near me

Area: errands
Checks hours and how busy it is.

Run:  python usecases/073_find_open_now/usecase.py                  # your preferred framework
      python usecases/073_find_open_now/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/073_find_open_now/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=73,
    area="errands",
    title="What's open near me",
    ask="Is the hardware store open now?",
    why="Checks hours and how busy it is.",
    tools=[T("place_hours", "Opening hours.", {"place": str, "city": str}, {"open_now": True, "closes": "20:00", "busy": "not busy"})],
    steps=[call("place_hours", place="Ace Hardware", city="{home_city}"), answer("Open until 8pm, and not busy right now.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
