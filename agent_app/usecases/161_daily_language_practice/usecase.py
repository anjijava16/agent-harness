"""Daily Spanish practice

Area: learning
Picks up where you left off (saved in memory) and saves progress.

Run:  python usecases/161_daily_language_practice/usecase.py                  # your preferred framework
      python usecases/161_daily_language_practice/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/161_daily_language_practice/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=161,
    area="learning",
    title="Daily Spanish practice",
    ask="Give me today's Spanish practice.",
    why="Picks up where you left off (saved in memory) and saves progress.",
    tools=[T("lesson", "Next lesson for a level.", {"level": str}, {"topic": "past tense: preterite", "words": 12})],
    steps=[recall("spanish"), call("lesson", level="A2"), remember("spanish", "A2; last: preterite"),
           answer("Today: the preterite, with 12 new words. Progress saved.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
