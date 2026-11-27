"""Overnight inbox triage

Area: mornings
Sorts mail into reply / read / archive and archives newsletters after one approval.

Run:  python usecases/008_inbox_zero_triage/usecase.py                  # your preferred framework
      python usecases/008_inbox_zero_triage/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/008_inbox_zero_triage/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=8,
    area="mornings",
    title="Overnight inbox triage",
    ask="Triage my overnight email.",
    why="Sorts mail into reply / read / archive and archives newsletters after one approval.",
    tools=[T("list_unread", "Unread emails.", {"since": str}, [{"id": 1, "from": "boss", "subj": "Q4 numbers?"}, {"id": 2, "from": "newsletter", "subj": "Weekly deals"},
                                                               {"id": 3, "from": "newsletter", "subj": "Tips"}]),
           T("archive", "Archive emails by id.", {"ids": list}, "archived", "write")],
    steps=[call("list_unread", since="yesterday 18:00"), call("archive", ids=[2, 3]),
           answer("One email needs a reply (your boss asking about Q4 numbers). Two newsletters archived.")],
    approvals={"archive": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
