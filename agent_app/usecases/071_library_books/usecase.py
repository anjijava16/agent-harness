"""Library books due

Area: errands
Checks the loans and renews the ones it can.

Run:  python usecases/071_library_books/usecase.py                  # your preferred framework
      python usecases/071_library_books/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/071_library_books/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=71,
    area="errands",
    title="Library books due",
    ask="Any library books due?",
    why="Checks the loans and renews the ones it can.",
    tools=[T("loans", "Library loans.", {"card": str}, [{"title": "The Overstory", "due": "tomorrow", "renewable": True}]),
           T("renew", "Renew a loan.", {"title": str}, "renewed", "write")],
    steps=[call("loans", card="main"), call("renew", title="The Overstory"),
           answer("The Overstory was due tomorrow. It's renewed for 3 weeks.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
