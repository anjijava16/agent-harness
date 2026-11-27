"""Physio exercise reminders

Area: health
Uses the routine your physio gave you (saved in memory).

Run:  python usecases/134_physio_exercises/usecase.py                  # your preferred framework
      python usecases/134_physio_exercises/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/134_physio_exercises/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=134,
    area="health",
    title="Physio exercise reminders",
    ask="Remind me to do my physio exercises every evening.",
    why="Uses the routine your physio gave you (saved in memory).",
    tools=[T("create_reminder", "Create a recurring reminder.", {"text": str, "time": str}, "created", "write")],
    steps=[recall("physio"), call("create_reminder", text="Physio: your saved routine", time="20:00"),
           answer("You'll get a reminder at 8pm every day for your physio routine.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
