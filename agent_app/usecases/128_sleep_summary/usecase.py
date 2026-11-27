"""Sleep summary

Area: health
Reads the sleep tracker for the last week.

Run:  python usecases/128_sleep_summary/usecase.py                  # your preferred framework
      python usecases/128_sleep_summary/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/128_sleep_summary/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=128,
    area="health",
    title="Sleep summary",
    ask="How have I been sleeping?",
    why="Reads the sleep tracker for the last week.",
    tools=[T("sleep_data", "Sleep tracker data.", {"days": int}, {"avg_hours": 6.4, "best": "Sat 7.9", "worst": "Wed 5.1"})],
    steps=[call("sleep_data", days=7),
           answer("Averaging 6.4 hours. Wednesday was the worst (5.1) and Saturday the best (7.9). A consistent bedtime would help.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
