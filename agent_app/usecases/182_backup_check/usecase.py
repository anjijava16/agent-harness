"""Are my backups working

Area: digital
Checks both backup services.

Run:  python usecases/182_backup_check/usecase.py                  # your preferred framework
      python usecases/182_backup_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/182_backup_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=182,
    area="digital",
    title="Are my backups working",
    ask="Did my laptop and phone back up this week?",
    why="Checks both backup services.",
    tools=[T("last_backup", "Last backup of a device.", {"device": str}, lambda device: {"laptop": "2 days ago", "phone": "19 days ago"}[device])],
    steps=[par(call("last_backup", device="laptop"), call("last_backup", device="phone")),
           answer("The laptop backed up 2 days ago. The phone hasn't backed up for 19 days, so plug it in on Wi-Fi tonight.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
