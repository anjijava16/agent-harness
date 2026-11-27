"""Register a new purchase's warranty

Area: digital
Pulls the serial number from the receipt and registers it.

Run:  python usecases/195_warranty_registry/usecase.py                  # your preferred framework
      python usecases/195_warranty_registry/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/195_warranty_registry/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=195,
    area="digital",
    title="Register a new purchase's warranty",
    ask="Register the warranty for the new TV.",
    why="Pulls the serial number from the receipt and registers it.",
    tools=[T("search_receipts", "Search receipts.", {"query": str}, [{"item": "65in TV", "serial": "TV9X22", "date": "2026-11-21"}]),
           T("register_warranty", "Register a warranty.", {"item": str, "serial": str}, "registered", "external")],
    steps=[call("search_receipts", query="TV"), call("register_warranty", item="65in TV", serial="TV9X22"),
           answer("TV warranty registered (serial TV9X22).")],
    approvals={"register_warranty": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
