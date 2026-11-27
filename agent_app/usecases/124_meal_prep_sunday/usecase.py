"""Sunday meal prep

Area: health
Recipes that fit your diet and keep for 4 days.

Run:  python usecases/124_meal_prep_sunday/usecase.py                  # your preferred framework
      python usecases/124_meal_prep_sunday/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/124_meal_prep_sunday/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=124,
    area="health",
    title="Sunday meal prep",
    ask="Plan a meal prep for weekday lunches.",
    why="Recipes that fit your diet and keep for 4 days.",
    tools=[T("recipe_search", "Recipes.", {"diet": str, "keeps_days": int}, ["chickpea curry", "farro salad with roasted veg"])],
    steps=[call("recipe_search", diet="{diet}", keeps_days=4),
           answer("Make a chickpea curry and a farro salad with roasted veg. Both keep 4 days and both are {diet}.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
