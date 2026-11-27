"""Summarize a meeting transcript

Area: inbox
Reads the transcript and pulls out only your items.

Run:  python usecases/024_meeting_notes_summary/usecase.py                  # your preferred framework
      python usecases/024_meeting_notes_summary/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/024_meeting_notes_summary/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=24,
    area="inbox",
    title="Summarize a meeting transcript",
    ask="Summarize the budget meeting and list my action items.",
    why="Reads the transcript and pulls out only your items.",
    tools=[T("get_transcript", "Meeting transcript.", {"meeting": str}, "Sam to send vendor quotes by Fri. Lee to book venue. Sam to update the budget sheet.")],
    steps=[call("get_transcript", meeting="budget-sync"),
           answer("Your items: send vendor quotes by Friday, and update the budget sheet. Lee is booking the venue.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
