"""Daily chess puzzle

Area: learning
Uses your rating from memory.

Run:  python usecases/175_chess_puzzle_daily/usecase.py                  # your preferred framework
      python usecases/175_chess_puzzle_daily/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/175_chess_puzzle_daily/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=175,
    area="learning",
    title="Daily chess puzzle",
    ask="Give me today's chess puzzle at my level.",
    why="Uses your rating from memory.",
    tools=[T("puzzle", "A puzzle at a rating.", {"rating": int}, {"theme": "fork", "moves": 2})],
    steps=[recall("chess"), call("puzzle", rating=1350), answer("Today's puzzle: a fork in 2 moves at about 1350.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
