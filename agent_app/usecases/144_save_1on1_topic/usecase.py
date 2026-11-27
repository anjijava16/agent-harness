"""Save a 1:1 topic

Area: work
Saved to memory for the 1:1 prep task.

Run:  python usecases/144_save_1on1_topic/usecase.py                  # your preferred framework
      python usecases/144_save_1on1_topic/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/144_save_1on1_topic/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=144,
    area="work",
    title="Save a 1:1 topic",
    ask="For my next 1:1: ask about the training budget.",
    why="Saved to memory for the 1:1 prep task.",
    tools=[],
    steps=[remember("1on1", "ask about training budget"), answer("Saved for your next 1:1.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
