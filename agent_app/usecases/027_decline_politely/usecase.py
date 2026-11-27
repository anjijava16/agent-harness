"""Decline a meeting politely

Area: inbox
Uses your saved tone preference from memory.

Run:  python usecases/027_decline_politely/usecase.py                  # your preferred framework
      python usecases/027_decline_politely/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/027_decline_politely/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=27,
    area="inbox",
    title="Decline a meeting politely",
    ask="Decline Friday's optional all-hands and say why.",
    why="Uses your saved tone preference from memory.",
    tools=[T("rsvp", "RSVP to an event.", {"event": str, "response": str, "note": str}, "done", "external")],
    steps=[recall("tone"), call("rsvp", event="Friday all-hands", response="no", note="Deadline that afternoon; I'll watch the recording."),
           answer("Declined, with a note that you'll watch the recording.")],
    approvals={"rsvp": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
