"""Habit tracker check-in

Area: mornings
Writes to the habit log and reads the streaks back.

Run:  python usecases/014_habit_streak/usecase.py                  # your preferred framework
      python usecases/014_habit_streak/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/014_habit_streak/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=14,
    area="mornings",
    title="Habit tracker check-in",
    ask="Log that I meditated and show my streaks.",
    why="Writes to the habit log and reads the streaks back.",
    tools=[T("log_habit", "Log a habit for today.", {"habit": str}, "logged", "write"),
           T("streaks", "Current habit streaks.", {"user": str}, {"meditate": 12, "read": 4, "run": 0})],
    steps=[call("log_habit", habit="meditate"), call("streaks", user="me"),
           answer("Logged. Meditation is on a 12-day streak and reading on 4. Running has dropped to 0.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
