"""Dinner near my hotel

Area: travel
Uses your diet preference.

Run:  python usecases/094_local_recs/usecase.py                  # your preferred framework
      python usecases/094_local_recs/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/094_local_recs/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=94,
    area="travel",
    title="Dinner near my hotel",
    ask="Good vegetarian dinner near the Maven?",
    why="Uses your diet preference.",
    tools=[T("restaurants", "Restaurants nearby.", {"near": str, "diet": str}, [{"name": "Watercourse Foods", "walk_min": 9}])],
    steps=[call("restaurants", near="Maven Hotel Denver", diet="{diet}"), answer("Watercourse Foods is 9 minutes' walk and fully {diet}.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
