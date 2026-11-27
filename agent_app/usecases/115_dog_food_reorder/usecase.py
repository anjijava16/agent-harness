"""Dog food running low

Area: home
Reads the smart feeder and reorders after approval.

Run:  python usecases/115_dog_food_reorder/usecase.py                  # your preferred framework
      python usecases/115_dog_food_reorder/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/115_dog_food_reorder/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=115,
    area="home",
    title="Dog food running low",
    ask="Are we low on dog food?",
    why="Reads the smart feeder and reorders after approval.",
    tools=[T("feeder_level", "Smart feeder food level.", {"pet": str}, {"days_left": 4}),
           T("reorder", "Reorder an item.", {"item": str, "amount": float}, "ordered", "money")],
    steps=[call("feeder_level", pet="{dog}"), call("reorder", item="dog food 24lb", amount=54.0),
           answer("{dog} has about 4 days of food left. A 24 lb bag is ordered.")],
    approvals={"reorder": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
