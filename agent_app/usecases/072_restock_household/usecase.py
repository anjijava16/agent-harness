"""Restock household basics

Area: errands
Reorders your usual basics from memory. You drop one item before it orders.

Run:  python usecases/072_restock_household/usecase.py                  # your preferred framework
      python usecases/072_restock_household/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/072_restock_household/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=72,
    area="errands",
    title="Restock household basics",
    ask="Restock the usual household stuff.",
    why="Reorders your usual basics from memory. You drop one item before it orders.",
    tools=[T("reorder", "Reorder an item.", {"item": str, "amount": float}, "ordered", "money")],
    steps=[recall("household"),
           par(call("reorder", item="dish soap", amount=8.5), call("reorder", item="paper towels", amount=19.0), call("reorder", item="dog food", amount=54.0)),
           answer("Reordered dish soap and dog food. You skipped the paper towels.")],
    approvals={"reorder": ["approve", "reject", "approve"]}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
