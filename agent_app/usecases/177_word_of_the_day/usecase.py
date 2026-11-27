"""Word of the day

Area: learning
A small daily habit; known words are kept in memory to avoid repeats.

Run:  python usecases/177_word_of_the_day/usecase.py                  # your preferred framework
      python usecases/177_word_of_the_day/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/177_word_of_the_day/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=177,
    area="learning",
    title="Word of the day",
    ask="Teach me a useful word today.",
    why="A small daily habit; known words are kept in memory to avoid repeats.",
    tools=[T("word", "A word you haven't seen.", {"lang": str}, {"word": "sobremesa", "meaning": "time spent talking at the table after a meal"})],
    steps=[recall("words_seen"), call("word", lang="es"), remember("words_seen", "sobremesa"),
           answer("Sobremesa: the time spent talking at the table after a meal.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
