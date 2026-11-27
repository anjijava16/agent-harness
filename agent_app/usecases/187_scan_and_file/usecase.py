"""Scan and file a letter

Area: digital
Reads the scan, names it properly and files it.

Run:  python usecases/187_scan_and_file/usecase.py                  # your preferred framework
      python usecases/187_scan_and_file/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/187_scan_and_file/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=187,
    area="digital",
    title="Scan and file a letter",
    ask="File the insurance letter I just scanned.",
    why="Reads the scan, names it properly and files it.",
    tools=[T("read_scan", "Read a scanned document.", {"scan": str}, {"from": "HomeShield Insurance", "date": "2026-11-20", "topic": "policy renewal"}),
           T("file_doc", "Save a document to a folder.", {"name": str, "folder": str}, "filed", "write")],
    steps=[call("read_scan", scan="latest"), call("file_doc", name="2026-11-20 HomeShield - policy renewal.pdf", folder="Insurance"),
           answer("Filed as '2026-11-20 HomeShield - policy renewal.pdf' in Insurance.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
