"""Restaurant that fits my diet

Area: health
Filters for your diet and books after approval.

Run:  python usecases/129_restaurant_for_diet/usecase.py                  # your preferred framework
      python usecases/129_restaurant_for_diet/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/129_restaurant_for_diet/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=129,
    area="health",
    title="Restaurant that fits my diet",
    ask="Dinner spot for 4 tonight, something everyone can eat.",
    why="Filters for your diet and books after approval.",
    tools=[T("restaurants", "Restaurants.", {"city": str, "diet": str, "party": int}, [{"name": "Handlebar", "time": "19:30"}]),
           T("reserve", "Reserve a table.", {"name": str, "time": str, "party": int}, "reserved", "external")],
    steps=[call("restaurants", city="{home_city}", diet="{diet}", party=4), call("reserve", name="Handlebar", time="19:30", party=4),
           answer("Handlebar is reserved for 4 at 19:30, with plenty of {diet} options.")],
    approvals={"reserve": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
