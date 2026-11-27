"""Draft replies to important email

Area: inbox
Drafts only. Nothing is sent without your OK, and one draft gets edited first.

Run:  python usecases/021_reply_drafts/usecase.py                  # your preferred framework
      python usecases/021_reply_drafts/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/021_reply_drafts/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=21,
    area="inbox",
    title="Draft replies to important email",
    ask="Draft replies to the emails that need me.",
    why="Drafts only. Nothing is sent without your OK, and one draft gets edited first.",
    tools=[T("needs_reply", "Emails waiting on you.", {"days": int}, [{"id": 7, "from": "landlord", "subj": "Lease renewal"}, {"id": 9, "from": "Coach Ellis", "subj": "Saturday carpool?"}]),
           T("send_email", "Send an email reply.", {"to": str, "body": str}, "sent", "external")],
    steps=[call("needs_reply", days=3),
           par(call("send_email", to="landlord", body="Yes, I'd like to renew for 12 months."), call("send_email", to="Coach Ellis", body="I can drive Saturday.")),
           answer("Both replies are sent. The landlord one went with your changes.")],
    approvals={"send_email": [("edit", {"body": "Happy to renew, but could we talk about the 6% increase first?"}), "approve"]}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
