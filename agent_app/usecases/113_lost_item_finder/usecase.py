"""Where did I leave my keys

Area: home
Asks the tracker tags.

Run:  python usecases/113_lost_item_finder/usecase.py                  # your preferred framework
      python usecases/113_lost_item_finder/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/113_lost_item_finder/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=113,
    area="home",
    title="Where did I leave my keys",
    ask="Where are my keys?",
    why="Asks the tracker tags.",
    tools=[T("tracker_location", "Location of a tracker tag.", {"tag": str}, {"place": "car, front seat", "seen": "40 min ago"})],
    steps=[call("tracker_location", tag="keys"), answer("In the car on the front seat, last seen 40 minutes ago.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
