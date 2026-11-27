"""Plan family dinners

Area: home
Uses saved family likes from memory and your diet.

Run:  python usecases/106_family_dinner_plan/usecase.py                  # your preferred framework
      python usecases/106_family_dinner_plan/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/106_family_dinner_plan/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=106,
    area="home",
    title="Plan family dinners",
    ask="Plan dinners for the week that Maya will actually eat.",
    why="Uses saved family likes from memory and your diet.",
    tools=[T("recipe_search", "Recipes.", {"diet": str, "likes": str}, ["veggie quesadillas", "mac and cheese with broccoli", "minestrone"])],
    steps=[recall("family_likes"), call("recipe_search", diet="{diet}", likes="cheese, pasta"),
           answer("This week: veggie quesadillas, mac and cheese with broccoli, minestrone. All {diet}, and all things {kid} likes.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
