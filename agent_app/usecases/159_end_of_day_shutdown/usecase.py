"""End-of-day shutdown

Area: work
Saves tomorrow's top task, sets your status and turns off work notifications.

Run:  python usecases/159_end_of_day_shutdown/usecase.py                  # your preferred framework
      python usecases/159_end_of_day_shutdown/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/159_end_of_day_shutdown/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=159,
    area="work",
    title="End-of-day shutdown",
    ask="Shut down my workday.",
    why="Saves tomorrow's top task, sets your status and turns off work notifications.",
    tools=[T("set_status", "Set chat status.", {"text": str, "until": str}, "set", "write"),
           T("dnd", "Do not disturb.", {"until": str}, "on", "write")],
    steps=[remember("tomorrow_top", "vendor quotes"),
           par(call("set_status", text="Offline", until="tomorrow 09:00"), call("dnd", until="tomorrow 09:00")),
           answer("You're offline until 9 tomorrow. Top task for tomorrow: vendor quotes.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
