"""Book club prep

Area: learning
Pulls the meeting date and saves your discussion notes.

Run:  python usecases/172_book_club_summary/usecase.py                  # your preferred framework
      python usecases/172_book_club_summary/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/172_book_club_summary/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=172,
    area="learning",
    title="Book club prep",
    ask="Prep me for book club: questions on Sea of Tranquility.",
    why="Pulls the meeting date and saves your discussion notes.",
    tools=[T("find_event", "Find an event.", {"query": str}, {"title": "Book club", "when": "Dec 4 19:00"})],
    steps=[call("find_event", query="book club"), remember("bookclub_notes", "time loops; pandemic chapters; favorite character"),
           answer("Book club is Dec 4 at 19:00. Your discussion notes are saved.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
