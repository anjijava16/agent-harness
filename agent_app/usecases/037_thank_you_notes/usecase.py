"""Thank-you notes after a party

Area: inbox
Reads the gift list you saved and sends the notes after one approval for the batch.

Run:  python usecases/037_thank_you_notes/usecase.py                  # your preferred framework
      python usecases/037_thank_you_notes/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/037_thank_you_notes/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=37,
    area="inbox",
    title="Thank-you notes after a party",
    ask="Draft thank-you notes for Maya's birthday gifts.",
    why="Reads the gift list you saved and sends the notes after one approval for the batch.",
    tools=[T("send_email", "Send an email.", {"to": str, "body": str}, "sent", "external")],
    steps=[recall("gifts"),
           par(call("send_email", to="Rosa", body="Thank you for the art set! Maya loves it."), call("send_email", to="the Chens", body="Thank you for the book!")),
           answer("Two thank-you notes sent.")],
    approvals={"send_email": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
