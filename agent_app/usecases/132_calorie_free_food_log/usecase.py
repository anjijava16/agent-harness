"""Log what I ate

Area: health
Writes a simple food log. No targets, just a record.

Run:  python usecases/132_calorie_free_food_log/usecase.py                  # your preferred framework
      python usecases/132_calorie_free_food_log/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/132_calorie_free_food_log/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=132,
    area="health",
    title="Log what I ate",
    ask="Log lunch: lentil soup and bread.",
    why="Writes a simple food log. No targets, just a record.",
    tools=[T("log_meal", "Log a meal.", {"meal": str, "items": str}, "logged", "write")],
    steps=[call("log_meal", meal="lunch", items="lentil soup, bread"), answer("Logged lunch.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
