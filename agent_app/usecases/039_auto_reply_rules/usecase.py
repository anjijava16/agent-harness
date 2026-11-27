"""Remember how I like to reply

Area: inbox
A standing preference, saved so every drafting task uses it.

Run:  python usecases/039_auto_reply_rules/usecase.py                  # your preferred framework
      python usecases/039_auto_reply_rules/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/039_auto_reply_rules/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=39,
    area="inbox",
    title="Remember how I like to reply",
    ask="Remember: keep my replies short and sign off with just 'Sam'.",
    why="A standing preference, saved so every drafting task uses it.",
    tools=[],
    steps=[remember("tone", "short replies, sign off 'Sam'"), answer("Got it: short replies, signed 'Sam'.")],
    expect=[("tone saved", lambda c: "short" in c["memories"].get("tone", ""))]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
