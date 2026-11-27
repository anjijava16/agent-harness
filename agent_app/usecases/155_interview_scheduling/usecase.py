"""Schedule interviews

Area: work
Finds your free slots and sends invites after approval.

Run:  python usecases/155_interview_scheduling/usecase.py                  # your preferred framework
      python usecases/155_interview_scheduling/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/155_interview_scheduling/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=155,
    area="work",
    title="Schedule interviews",
    ask="Schedule 3 candidate interviews for next week.",
    why="Finds your free slots and sends invites after approval.",
    tools=[T("free_slots", "Free slots.", {"week": str}, ["Tue 14:00", "Wed 11:00", "Thu 15:00"]),
           T("send_invite", "Send an invite.", {"when": str, "people": str, "title": str}, "invited", "external")],
    steps=[call("free_slots", week="next"),
           par(call("send_invite", when="Tue 14:00", people="cand-a", title="Interview"), call("send_invite", when="Wed 11:00", people="cand-b", title="Interview"),
               call("send_invite", when="Thu 15:00", people="cand-c", title="Interview")),
           answer("Three interviews booked: Tuesday 14:00, Wednesday 11:00 and Thursday 15:00.")],
    approvals={"send_invite": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
