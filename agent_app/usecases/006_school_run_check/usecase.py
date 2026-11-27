"""School run check

Area: mornings
Reads the school portal and your memory of what she needs on gym days.

Run:  python usecases/006_school_run_check/usecase.py                  # your preferred framework
      python usecases/006_school_run_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/006_school_run_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=6,
    area="mornings",
    title="School run check",
    ask="Anything I need for Maya's school today?",
    why="Reads the school portal and your memory of what she needs on gym days.",
    tools=[T("school_notices", "Notices from the school portal.", {"student": str}, ["Field trip permission slip due Friday", "Gym today"])],
    steps=[par(call("school_notices", student="{kid}"), recall("gym")),
           answer("{kid} has gym today, so pack sneakers. The field trip slip is due Friday.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
