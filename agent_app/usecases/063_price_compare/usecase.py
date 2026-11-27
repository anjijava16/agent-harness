"""Find the best price

Area: errands
Checks several stores at once.

Run:  python usecases/063_price_compare/usecase.py                  # your preferred framework
      python usecases/063_price_compare/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/063_price_compare/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=63,
    area="errands",
    title="Find the best price",
    ask="Where's the cheapest place to buy a 65-inch TV?",
    why="Checks several stores at once.",
    tools=[T("store_price", "Price at a store.", {"store": str, "item": str}, lambda store, item: {"A": 549, "B": 499, "C": 529}[store])],
    steps=[par(call("store_price", store="A", item="65in TV"), call("store_price", store="B", item="65in TV"), call("store_price", store="C", item="65in TV")),
           answer("Store B has it for $499, which is $50 under Store A.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
