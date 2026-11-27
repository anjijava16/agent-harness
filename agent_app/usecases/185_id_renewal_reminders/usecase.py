"""Document renewal dates

Area: digital
Reads the expiry dates you saved and sets reminders.

Run:  python usecases/185_id_renewal_reminders/usecase.py                  # your preferred framework
      python usecases/185_id_renewal_reminders/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/185_id_renewal_reminders/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=185,
    area="digital",
    title="Document renewal dates",
    ask="When do my license and passport need renewing?",
    why="Reads the expiry dates you saved and sets reminders.",
    tools=[T("create_reminder", "Create a reminder.", {"text": str, "date": str}, "created", "write")],
    steps=[recall("expiry"),
           par(call("create_reminder", text="Renew driver's license", date="2027-01-15"), call("create_reminder", text="Renew passport", date="2027-03-01")),
           answer("Reminders set: license renewal in mid-January 2027, passport in March 2027.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
