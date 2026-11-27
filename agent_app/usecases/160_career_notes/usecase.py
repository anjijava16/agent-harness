"""Brag doc entry

Area: work
Saves wins as they happen, so review season is easy.

Run:  python usecases/160_career_notes/usecase.py                  # your preferred framework
      python usecases/160_career_notes/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/160_career_notes/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=160,
    area="work",
    title="Brag doc entry",
    ask="Add to my brag doc: led the Q4 review across 4 teams.",
    why="Saves wins as they happen, so review season is easy.",
    tools=[],
    steps=[remember("brag_q4", "Led the Q4 review across 4 teams"), answer("Added to your brag doc.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
