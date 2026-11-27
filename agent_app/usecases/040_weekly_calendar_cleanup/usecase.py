"""Clear out stale recurring meetings

Area: inbox
Finds recurring meetings you skip and declines them after approval; one you keep.

Run:  python usecases/040_weekly_calendar_cleanup/usecase.py                  # your preferred framework
      python usecases/040_weekly_calendar_cleanup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/040_weekly_calendar_cleanup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=40,
    area="inbox",
    title="Clear out stale recurring meetings",
    ask="Which recurring meetings could I drop?",
    why="Finds recurring meetings you skip and declines them after approval; one you keep.",
    tools=[T("recurring_attendance", "Your attendance at recurring meetings.", {"weeks": int}, [{"title": "Design crit", "attended": "1/8"}, {"title": "Book club", "attended": "2/8"}]),
           T("leave_series", "Leave a recurring meeting.", {"title": str}, "left", "external")],
    steps=[call("recurring_attendance", weeks=8),
           par(call("leave_series", title="Design crit"), call("leave_series", title="Book club")),
           answer("You left Design crit. You kept Book club.")],
    approvals={"leave_series": ["approve", "reject"]}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
