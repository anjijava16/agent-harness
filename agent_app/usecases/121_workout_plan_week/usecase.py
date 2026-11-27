"""This week's workouts

Area: health
Fits workouts into free slots and saves the plan.

Run:  python usecases/121_workout_plan_week/usecase.py                  # your preferred framework
      python usecases/121_workout_plan_week/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/121_workout_plan_week/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=121,
    area="health",
    title="This week's workouts",
    ask="Plan my workouts around my calendar.",
    why="Fits workouts into free slots and saves the plan.",
    tools=[T("free_slots", "Your free slots this week.", {"week": str}, ["Mon 7:00", "Wed 18:00", "Sat 9:00"])],
    steps=[par(call("free_slots", week="this"), recall("workout")),
           remember("workouts_week", "Mon 7:00 run; Wed 18:00 strength; Sat 9:00 long run"),
           answer("Monday 7:00 run, Wednesday 18:00 strength, Saturday 9:00 long run. They're saved and fit your calendar.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
