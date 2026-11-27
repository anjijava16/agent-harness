"""Set a fitness goal

Area: health
Saved so workout planning works towards it.

Run:  python usecases/140_save_fitness_goal/usecase.py                  # your preferred framework
      python usecases/140_save_fitness_goal/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/140_save_fitness_goal/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=140,
    area="health",
    title="Set a fitness goal",
    ask="My goal: run a 10K under 55 minutes by April.",
    why="Saved so workout planning works towards it.",
    tools=[],
    steps=[remember("workout", "goal: 10K under 55 min by April"), answer("Saved: a 10K under 55 minutes by April.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
