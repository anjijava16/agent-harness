"""Follow up after a conference

Area: work
Uses the contacts you saved and sends notes after approval.

Run:  python usecases/149_networking_follow_up/usecase.py                  # your preferred framework
      python usecases/149_networking_follow_up/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/149_networking_follow_up/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=149,
    area="work",
    title="Follow up after a conference",
    ask="Follow up with the people I met at the conference.",
    why="Uses the contacts you saved and sends notes after approval.",
    tools=[T("send_email", "Send an email.", {"to": str, "body": str}, "sent", "external")],
    steps=[recall("conference"),
           par(call("send_email", to="Dana Kim", body="Great meeting you at the summit!"), call("send_email", to="Raj Patel", body="Thanks for the chat about pricing.")),
           answer("Follow-ups sent to Dana Kim and Raj Patel.")],
    approvals={"send_email": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
