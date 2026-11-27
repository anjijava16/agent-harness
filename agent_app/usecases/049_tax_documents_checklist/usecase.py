"""Tax documents checklist

Area: money
Compares what has arrived with last year's list from memory.

Run:  python usecases/049_tax_documents_checklist/usecase.py                  # your preferred framework
      python usecases/049_tax_documents_checklist/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/049_tax_documents_checklist/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=49,
    area="money",
    title="Tax documents checklist",
    ask="Which tax documents do I still need?",
    why="Compares what has arrived with last year's list from memory.",
    tools=[T("tax_docs_received", "Tax documents received so far.", {"year": int}, ["W-2", "1099-INT bank"])],
    steps=[par(recall("tax"), call("tax_docs_received", year=2026)),
           answer("You have the W-2 and the bank 1099-INT. Still to come: the brokerage 1099 and the mortgage interest form (1098).")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
