"""Summarize a long document

Area: work
Reads the doc and pulls out terms, dates and anything unusual.

Run:  python usecases/145_document_summary/usecase.py                  # your preferred framework
      python usecases/145_document_summary/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/145_document_summary/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=145,
    area="work",
    title="Summarize a long document",
    ask="Summarize the 40-page vendor contract.",
    why="Reads the doc and pulls out terms, dates and anything unusual.",
    tools=[T("read_doc", "Read a document.", {"doc": str}, {"pages": 40, "term": "24 months", "auto_renew": True, "notice_days": 90, "liability_cap": "fees paid"})],
    steps=[call("read_doc", doc="vendor-contract.pdf"),
           answer("24-month term that renews automatically unless you give 90 days' notice. Liability is capped at fees paid. The auto-renewal is the thing to watch.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
