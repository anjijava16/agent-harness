"""Out-of-office for a sick day

Area: mornings
Sets the auto-reply, declines today's meetings, and messages your manager. The message waits for
your edit.

Run:  python usecases/017_set_out_of_office/usecase.py                  # your preferred framework
      python usecases/017_set_out_of_office/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/017_set_out_of_office/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=17,
    area="mornings",
    title="Out-of-office for a sick day",
    ask="I'm out sick today. Handle it.",
    why="Sets the auto-reply, declines today's meetings, and messages your manager. The message waits for your edit.",
    tools=[T("set_ooo", "Set an email auto-reply.", {"message": str, "until": str}, "set", "write"),
           T("decline_today", "Decline today's meetings.", {"note": str}, {"declined": 3}, "external"),
           T("message_manager", "Message your manager.", {"text": str}, "sent", "external")],
    steps=[par(call("set_ooo", message="Out sick today, back tomorrow.", until="tomorrow"), call("decline_today", note="Out sick")),
           call("message_manager", text="I'm out sick today."),
           answer("Auto-reply on, 3 meetings declined, and your manager has your message.")],
    approvals={"decline_today": "approve", "message_manager": ("edit", {"text": "Out sick today. The report draft is on track for Thursday; Jo can cover standup."})}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
