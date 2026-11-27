"""Which meetings cost the most time

Area: work
Sums meeting hours by series.

Run:  python usecases/158_meeting_cost/usecase.py                  # your preferred framework
      python usecases/158_meeting_cost/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/158_meeting_cost/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=158,
    area="work",
    title="Which meetings cost the most time",
    ask="Which meetings take most of my week?",
    why="Sums meeting hours by series.",
    tools=[T("meeting_hours", "Hours per meeting series.", {"weeks": int}, {"Weekly sync": 6, "Design crit": 3, "1:1s": 2})],
    steps=[call("meeting_hours", weeks=4),
           answer("Weekly sync takes 6 hours a month. Asking to make it 30 minutes would save 3 hours.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
