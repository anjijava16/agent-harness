"""Remember my travel preferences

Area: travel
Saved to memory so flight searches follow it.

Run:  python usecases/099_save_travel_prefs/usecase.py                  # your preferred framework
      python usecases/099_save_travel_prefs/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/099_save_travel_prefs/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=99,
    area="travel",
    title="Remember my travel preferences",
    ask="Remember: aisle seat, no red-eyes, carry-on only.",
    why="Saved to memory so flight searches follow it.",
    tools=[],
    steps=[remember("travel_prefs", "aisle; no red-eyes; carry-on only"), answer("Saved: aisle, no red-eyes, carry-on only.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
