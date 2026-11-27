"""Drink-water reminders

Area: health
Creates reminders inside your work hours only.

Run:  python usecases/125_water_reminder/usecase.py                  # your preferred framework
      python usecases/125_water_reminder/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/125_water_reminder/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=125,
    area="health",
    title="Drink-water reminders",
    ask="Remind me to drink water every 2 hours during work.",
    why="Creates reminders inside your work hours only.",
    tools=[T("create_reminder", "Create a recurring reminder.", {"text": str, "every": str, "window": str}, "created", "write")],
    steps=[call("create_reminder", text="Drink water", every="2h", window="{work_hours}"),
           answer("You'll get a water reminder every 2 hours between {work_hours}.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
