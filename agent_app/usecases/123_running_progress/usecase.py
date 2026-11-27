"""Running progress

Area: health
Reads workout data and compares it with last month.

Run:  python usecases/123_running_progress/usecase.py                  # your preferred framework
      python usecases/123_running_progress/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/123_running_progress/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=123,
    area="health",
    title="Running progress",
    ask="How's my running going this month?",
    why="Reads workout data and compares it with last month.",
    tools=[T("runs", "Runs in a month.", {"month": str}, lambda month: {"this": {"km": 62, "avg_pace": "5:41"}, "last": {"km": 48, "avg_pace": "5:55"}}[month])],
    steps=[par(call("runs", month="this"), call("runs", month="last")),
           answer("62 km this month, up from 48, and your average pace improved from 5:55 to 5:41 per km.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
