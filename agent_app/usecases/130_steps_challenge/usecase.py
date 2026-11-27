"""Step challenge with friends

Area: health
Creates the challenge and invites them after approval.

Run:  python usecases/130_steps_challenge/usecase.py                  # your preferred framework
      python usecases/130_steps_challenge/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/130_steps_challenge/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=130,
    area="health",
    title="Step challenge with friends",
    ask="Start a 7-day step challenge with Lee and Ana.",
    why="Creates the challenge and invites them after approval.",
    tools=[T("create_challenge", "Create a step challenge.", {"days": int, "people": list}, "created", "external")],
    steps=[call("create_challenge", days=7, people=["Lee", "Ana"]), answer("The 7-day challenge has started with Lee and Ana.")],
    approvals={"create_challenge": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
