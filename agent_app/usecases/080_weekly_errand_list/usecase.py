"""Weekly errand list

Area: errands
Saves the list to memory so other tasks (route planning, reminders) can use it.

Run:  python usecases/080_weekly_errand_list/usecase.py                  # your preferred framework
      python usecases/080_weekly_errand_list/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/080_weekly_errand_list/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=80,
    area="errands",
    title="Weekly errand list",
    ask="Save this week's errands: post office, return shoes, pick up dry cleaning.",
    why="Saves the list to memory so other tasks (route planning, reminders) can use it.",
    tools=[],
    steps=[remember("errands_week", "post office; return shoes; dry cleaning"), answer("Saved 3 errands for this week.")],
    expect=[("errands saved", lambda c: "dry cleaning" in c["memories"].get("errands_week", ""))]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
