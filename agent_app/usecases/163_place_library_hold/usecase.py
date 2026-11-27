"""Place a library hold

Area: learning
A small action, but it's on your account, so it needs approval.

Run:  python usecases/163_place_library_hold/usecase.py                  # your preferred framework
      python usecases/163_place_library_hold/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/163_place_library_hold/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=163,
    area="learning",
    title="Place a library hold",
    ask="Put Klara and the Sun on hold.",
    why="A small action, but it's on your account, so it needs approval.",
    tools=[T("place_hold", "Place a library hold.", {"title": str}, {"position": 4}, "external")],
    steps=[call("place_hold", title="Klara and the Sun"), answer("Hold placed. You're 4th in line.")],
    approvals={"place_hold": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
