"""Grocery list from this week's meals

Area: errands
Reads the meal plan and pantry and adds only what's missing, for your diet.

Run:  python usecases/061_grocery_list_from_meals/usecase.py                  # your preferred framework
      python usecases/061_grocery_list_from_meals/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/061_grocery_list_from_meals/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=61,
    area="errands",
    title="Grocery list from this week's meals",
    ask="Make my grocery list for this week's meal plan.",
    why="Reads the meal plan and pantry and adds only what's missing, for your diet.",
    tools=[T("meal_plan", "This week's meal plan.", {"diet": str}, ["lentil soup", "veggie tacos", "pasta primavera"]),
           T("pantry", "Pantry items.", {"location": str}, ["lentils", "pasta", "olive oil"])],
    steps=[par(call("meal_plan", diet="{diet}"), call("pantry", location="home")),
           remember("grocery_list", "carrots, celery, tortillas, black beans, zucchini, parmesan"),
           answer("Need: carrots, celery, tortillas, black beans, zucchini and parmesan. You already have lentils and pasta.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
