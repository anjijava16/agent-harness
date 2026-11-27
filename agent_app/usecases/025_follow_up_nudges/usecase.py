"""Follow-ups I'm waiting on

Area: inbox
Finds sent emails with no answer and sends polite nudges after approval.

Run:  python usecases/025_follow_up_nudges/usecase.py                  # your preferred framework
      python usecases/025_follow_up_nudges/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/025_follow_up_nudges/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=25,
    area="inbox",
    title="Follow-ups I'm waiting on",
    ask="Who hasn't replied to me this week?",
    why="Finds sent emails with no answer and sends polite nudges after approval.",
    tools=[T("awaiting_reply", "Sent emails with no reply.", {"days": int}, [{"to": "contractor", "subj": "Quote for deck"}]),
           T("send_email", "Send an email.", {"to": str, "body": str}, "sent", "external")],
    steps=[call("awaiting_reply", days=7), call("send_email", to="contractor", body="Just checking in on the deck quote."),
           answer("One open thread: the contractor's deck quote. Nudge sent.")],
    approvals={"send_email": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
