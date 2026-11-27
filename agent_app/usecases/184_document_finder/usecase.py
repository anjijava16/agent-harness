"""Find a document

Area: digital
Searches the documents drive.

Run:  python usecases/184_document_finder/usecase.py                  # your preferred framework
      python usecases/184_document_finder/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/184_document_finder/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=184,
    area="digital",
    title="Find a document",
    ask="Find my car title document.",
    why="Searches the documents drive.",
    tools=[T("search_docs", "Search your documents.", {"query": str}, [{"name": "Car title - Honda.pdf", "folder": "Important/Vehicle"}])],
    steps=[call("search_docs", query="car title"), answer("Found it: 'Car title - Honda.pdf' in Important/Vehicle.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
