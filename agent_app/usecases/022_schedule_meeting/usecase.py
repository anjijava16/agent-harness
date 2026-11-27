"""Find a time and book a meeting

Area: inbox
Finds shared free time in your work hours. The invite waits for approval.

Run:  python usecases/022_schedule_meeting/usecase.py                  # your preferred framework
      python usecases/022_schedule_meeting/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/022_schedule_meeting/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=22,
    area="inbox",
    title="Find a time and book a meeting",
    ask="Book an hour with Priya and Tom next week.",
    why="Finds shared free time in your work hours. The invite waits for approval.",
    tools=[T("free_slots", "Shared free slots.", {"people": str, "week": str}, ["Tue 10:00", "Wed 15:00"]),
           T("send_invite", "Send a calendar invite.", {"when": str, "people": str, "title": str}, "invited", "external")],
    steps=[call("free_slots", people="priya,tom", week="next"), call("send_invite", when="Tue 10:00", people="priya,tom", title="Planning"),
           answer("Invite sent for Tuesday 10:00 with Priya and Tom.")],
    approvals={"send_invite": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
