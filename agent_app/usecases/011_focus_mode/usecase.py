"""Focus mode until noon

Area: mornings
Sets your Slack status and do-not-disturb, then moves one meeting after you approve.

Run:  python usecases/011_focus_mode/usecase.py                  # your preferred framework
      python usecases/011_focus_mode/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/011_focus_mode/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=11,
    area="mornings",
    title="Focus mode until noon",
    ask="Turn on focus mode until noon.",
    why="Sets your Slack status and do-not-disturb, then moves one meeting after you approve.",
    tools=[T("set_status", "Set chat status.", {"text": str, "until": str}, "set", "write"),
           T("dnd", "Do not disturb until a time.", {"until": str}, "on", "write"),
           T("move_meeting", "Move a meeting.", {"title": str, "to": str}, "moved", "external")],
    steps=[par(call("set_status", text="Heads down", until="12:00"), call("dnd", until="12:00")),
           call("move_meeting", title="Vendor sync", to="14:30"),
           answer("Focus on until noon: status set, notifications off, and the vendor sync moved to 14:30.")],
    approvals={"move_meeting": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
