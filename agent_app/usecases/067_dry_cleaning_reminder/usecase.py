"""Dry cleaning reminder

Area: errands
Creates a location-based reminder.

Run:  python usecases/067_dry_cleaning_reminder/usecase.py                  # your preferred framework
      python usecases/067_dry_cleaning_reminder/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/067_dry_cleaning_reminder/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=67,
    area="errands",
    title="Dry cleaning reminder",
    ask="Remind me to pick up dry cleaning when I'm near it.",
    why="Creates a location-based reminder.",
    tools=[T("geo_reminder", "Reminder at a place.", {"text": str, "place": str}, "created", "write")],
    steps=[call("geo_reminder", text="Pick up dry cleaning", place="Spotless Cleaners"),
           answer("I'll remind you when you're near Spotless Cleaners.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
