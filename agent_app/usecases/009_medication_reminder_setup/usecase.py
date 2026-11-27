"""Daily reminders setup

Area: mornings
Recreates reminders from memory, so you don't retype them on a new phone.

Run:  python usecases/009_medication_reminder_setup/usecase.py                  # your preferred framework
      python usecases/009_medication_reminder_setup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/009_medication_reminder_setup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=9,
    area="mornings",
    title="Daily reminders setup",
    ask="Set my usual daily reminders.",
    why="Recreates reminders from memory, so you don't retype them on a new phone.",
    tools=[T("create_reminder", "Create a recurring reminder.", {"text": str, "time": str}, "created", "write")],
    steps=[recall("reminders"),
           par(call("create_reminder", text="Take vitamins", time="08:00"), call("create_reminder", text="Walk {dog}", time="18:30")),
           answer("Two daily reminders set: vitamins at 8:00 and walking {dog} at 18:30.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
