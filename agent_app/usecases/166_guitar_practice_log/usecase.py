"""Guitar practice log

Area: learning
Keeps a practice log and shows the weekly total.

Run:  python usecases/166_guitar_practice_log/usecase.py                  # your preferred framework
      python usecases/166_guitar_practice_log/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/166_guitar_practice_log/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=166,
    area="learning",
    title="Guitar practice log",
    ask="Log 30 minutes of guitar: worked on barre chords.",
    why="Keeps a practice log and shows the weekly total.",
    tools=[T("log_practice", "Log practice.", {"instrument": str, "minutes": int, "notes": str}, "logged", "write"),
           T("practice_week", "Practice minutes this week.", {"instrument": str}, 95)],
    steps=[call("log_practice", instrument="guitar", minutes=30, notes="barre chords"), call("practice_week", instrument="guitar"),
           answer("Logged. 95 minutes of guitar this week.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
