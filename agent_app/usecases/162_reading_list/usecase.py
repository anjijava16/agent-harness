"""What should I read next

Area: learning
Uses books you liked (saved in memory) and checks library availability.

Run:  python usecases/162_reading_list/usecase.py                  # your preferred framework
      python usecases/162_reading_list/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/162_reading_list/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=162,
    area="learning",
    title="What should I read next",
    ask="What should I read next?",
    why="Uses books you liked (saved in memory) and checks library availability.",
    tools=[T("book_recs", "Recommendations from liked books.", {"liked": str}, ["Sea of Tranquility", "Klara and the Sun"]),
           T("library_availability", "Library availability.", {"title": str}, lambda title: {"Sea of Tranquility": "available", "Klara and the Sun": "3 holds"}[title])],
    steps=[recall("books"), call("book_recs", liked="The Overstory"),
           par(call("library_availability", title="Sea of Tranquility"), call("library_availability", title="Klara and the Sun")),
           answer("Sea of Tranquility, which the library has right now. Klara and the Sun has 3 holds.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
