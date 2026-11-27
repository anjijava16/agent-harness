"""Breakfast from what's in the fridge

Area: mornings
Uses the fridge inventory and your diet preference.

Run:  python usecases/012_breakfast_idea/usecase.py                  # your preferred framework
      python usecases/012_breakfast_idea/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/012_breakfast_idea/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=12,
    area="mornings",
    title="Breakfast from what's in the fridge",
    ask="What can I make for breakfast?",
    why="Uses the fridge inventory and your diet preference.",
    tools=[T("fridge_inventory", "What's in the fridge.", {"location": str}, ["eggs", "spinach", "feta", "bread"]),
           T("recipe_search", "Recipes from ingredients.", {"ingredients": str, "diet": str}, ["Spinach and feta omelette (10 min)"])],
    steps=[call("fridge_inventory", location="kitchen"), call("recipe_search", ingredients="eggs, spinach, feta", diet="{diet}"),
           answer("Spinach and feta omelette with toast, 10 minutes, and it fits your {diet} diet.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
