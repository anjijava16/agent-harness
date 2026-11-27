"""Homework check

Area: home
Reads the school portal and tells you only what's due.

Run:  python usecases/105_kid_homework_check/usecase.py                  # your preferred framework
      python usecases/105_kid_homework_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/105_kid_homework_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=105,
    area="home",
    title="Homework check",
    ask="Does Maya have homework due tomorrow?",
    why="Reads the school portal and tells you only what's due.",
    tools=[T("assignments", "Assignments due.", {"student": str, "due": str}, [{"subject": "Math", "task": "worksheet p.42"}, {"subject": "Reading", "task": "20 minutes log"}])],
    steps=[call("assignments", student="{kid}", due="tomorrow"), answer("{kid} has a math worksheet (p.42) and 20 minutes of reading to log.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
