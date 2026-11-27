"""Book a pet sitter

Area: travel
Uses the sitter you saved in memory and books after approval.

Run:  python usecases/096_pet_sitter/usecase.py                  # your preferred framework
      python usecases/096_pet_sitter/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/096_pet_sitter/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=96,
    area="travel",
    title="Book a pet sitter",
    ask="Book a sitter for Biscuit while I'm in Denver.",
    why="Uses the sitter you saved in memory and books after approval.",
    tools=[T("sitter_availability", "Sitter availability.", {"sitter": str, "dates": str}, True),
           T("book_sitter", "Book the sitter.", {"sitter": str, "dates": str}, "booked", "money")],
    steps=[recall("sitter"), call("sitter_availability", sitter="Dana", dates="Dec 12-15"), call("book_sitter", sitter="Dana", dates="Dec 12-15"),
           answer("Dana is booked for {dog}, Dec 12-15.")],
    approvals={"book_sitter": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
