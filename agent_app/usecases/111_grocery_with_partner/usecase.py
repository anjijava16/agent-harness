"""Shared shopping list

Area: home
Writes to the shared list.

Run:  python usecases/111_grocery_with_partner/usecase.py                  # your preferred framework
      python usecases/111_grocery_with_partner/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/111_grocery_with_partner/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=111,
    area="home",
    title="Shared shopping list",
    ask="Add oat milk and coffee to the list Jordan and I share.",
    why="Writes to the shared list.",
    tools=[T("add_to_list", "Add items to a shared list.", {"list": str, "items": list}, "added", "write")],
    steps=[call("add_to_list", list="household", items=["oat milk", "coffee"]), answer("Added oat milk and coffee to the shared list.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
