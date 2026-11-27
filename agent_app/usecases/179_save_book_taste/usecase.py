"""Remember books I liked

Area: learning
Saved so book recommendations improve.

Run:  python usecases/179_save_book_taste/usecase.py                  # your preferred framework
      python usecases/179_save_book_taste/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/179_save_book_taste/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=179,
    area="learning",
    title="Remember books I liked",
    ask="Remember I loved The Overstory and Project Hail Mary.",
    why="Saved so book recommendations improve.",
    tools=[],
    steps=[remember("books", "loved: The Overstory, Project Hail Mary"), answer("Saved. Recommendations will use that.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
