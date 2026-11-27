"""Study schedule

Area: learning
Two sessions a week, in free evening slots.

Run:  python usecases/165_study_schedule/usecase.py                  # your preferred framework
      python usecases/165_study_schedule/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/165_study_schedule/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=165,
    area="learning",
    title="Study schedule",
    ask="Put my course study sessions on the calendar.",
    why="Two sessions a week, in free evening slots.",
    tools=[T("free_slots", "Free slots.", {"week": str}, ["Tue 20:00", "Sun 10:00"]),
           T("add_event", "Add a calendar event.", {"title": str, "when": str}, "added", "write")],
    steps=[call("free_slots", week="next"), par(call("add_event", title="Study", when="Tue 20:00"), call("add_event", title="Study", when="Sun 10:00")),
           answer("Study sessions added on Tuesday 20:00 and Sunday 10:00.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
