"""Block focus time

Area: work
Adds calendar holds in your free mornings.

Run:  python usecases/152_focus_time_blocks/usecase.py                  # your preferred framework
      python usecases/152_focus_time_blocks/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/152_focus_time_blocks/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=152,
    area="work",
    title="Block focus time",
    ask="Block 2 hours of focus time each morning next week.",
    why="Adds calendar holds in your free mornings.",
    tools=[T("free_slots", "Free slots.", {"week": str}, ["Mon 9-11", "Tue 9-11", "Thu 9-11"]),
           T("add_event", "Add a calendar event.", {"title": str, "when": str}, "added", "write")],
    steps=[call("free_slots", week="next"),
           par(call("add_event", title="Focus", when="Mon 9-11"), call("add_event", title="Focus", when="Tue 9-11"), call("add_event", title="Focus", when="Thu 9-11")),
           answer("Focus blocks added Monday, Tuesday and Thursday 9-11. Wednesday and Friday mornings are already full.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
