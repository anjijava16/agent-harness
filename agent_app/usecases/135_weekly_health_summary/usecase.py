"""Weekly wellness summary

Area: health
Three sources in parallel, one short summary.

Run:  python usecases/135_weekly_health_summary/usecase.py                  # your preferred framework
      python usecases/135_weekly_health_summary/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/135_weekly_health_summary/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=135,
    area="health",
    title="Weekly wellness summary",
    ask="Give me my week: sleep, steps, workouts.",
    why="Three sources in parallel, one short summary.",
    tools=[T("sleep_data", "Sleep data.", {"days": int}, {"avg_hours": 6.9}),
           T("steps", "Daily steps.", {"days": int}, {"avg": 8400}),
           T("workouts_done", "Workouts completed.", {"days": int}, 3)],
    steps=[par(call("sleep_data", days=7), call("steps", days=7), call("workouts_done", days=7)),
           answer("This week: 6.9 hours of sleep on average, 8,400 steps a day, and all 3 planned workouts done.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
