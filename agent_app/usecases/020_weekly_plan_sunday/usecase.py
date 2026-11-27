"""Sunday week-ahead plan

Area: mornings
Looks at the whole week, flags crunch days and saves a short plan.

Run:  python usecases/020_weekly_plan_sunday/usecase.py                  # your preferred framework
      python usecases/020_weekly_plan_sunday/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/020_weekly_plan_sunday/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=20,
    area="mornings",
    title="Sunday week-ahead plan",
    ask="Plan my week.",
    why="Looks at the whole week, flags crunch days and saves a short plan.",
    tools=[T("week_calendar", "Meetings per day this week.", {"week": str}, {"Mon": 6, "Tue": 2, "Wed": 7, "Thu": 3, "Fri": 1}),
           T("deadlines", "Deadlines this week.", {"week": str}, [{"what": "Quarterly report", "day": "Thu"}])],
    steps=[par(call("week_calendar", week="next"), call("deadlines", week="next")),
           remember("week_plan", "Deep work Tue+Thu AM; report due Thu; Wed is meeting-heavy"),
           answer("Wednesday is heavy (7 meetings). The report is due Thursday, so do deep work Tuesday and Thursday morning. Plan saved.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
