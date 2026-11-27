"""Gift ideas

Area: errands
Uses what you've saved about Jordan's interests.

Run:  python usecases/068_gift_ideas/usecase.py                  # your preferred framework
      python usecases/068_gift_ideas/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/068_gift_ideas/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=68,
    area="errands",
    title="Gift ideas",
    ask="Gift ideas for Jordan's birthday under $100?",
    why="Uses what you've saved about Jordan's interests.",
    tools=[T("gift_search", "Search gifts.", {"interests": str, "max_price": int}, ["Pottery class for two ($90)", "Trail running vest ($75)"])],
    steps=[recall("jordan"), call("gift_search", interests="pottery, trail running", max_price=100),
           answer("Two ideas: a pottery class for two ($90) or a trail running vest ($75).")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
