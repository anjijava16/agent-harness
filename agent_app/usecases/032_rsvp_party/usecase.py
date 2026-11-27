"""RSVP to a party

Area: inbox
Simple, but it's a message to someone else, so it waits for approval.

Run:  python usecases/032_rsvp_party/usecase.py                  # your preferred framework
      python usecases/032_rsvp_party/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/032_rsvp_party/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=32,
    area="inbox",
    title="RSVP to a party",
    ask="RSVP yes to the Chens' party for me and Jordan.",
    why="Simple, but it's a message to someone else, so it waits for approval.",
    tools=[T("rsvp", "RSVP to an invite.", {"event": str, "guests": int, "note": str}, "done", "external")],
    steps=[call("rsvp", event="Chen holiday party", guests=2, note="Sam and {partner} will be there!"),
           answer("RSVP sent: you and {partner}.")],
    approvals={"rsvp": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
