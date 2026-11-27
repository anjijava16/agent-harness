"""Sign Maya up for swim class

Area: home
Checks the schedule. Registration is a payment that needs approval.

Run:  python usecases/112_kid_activity_signup/usecase.py                  # your preferred framework
      python usecases/112_kid_activity_signup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/112_kid_activity_signup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=112,
    area="home",
    title="Sign Maya up for swim class",
    ask="Sign Maya up for the Saturday swim class.",
    why="Checks the schedule. Registration is a payment that needs approval.",
    tools=[T("class_schedule", "Classes at a center.", {"center": str, "activity": str}, [{"class": "Swim Level 2", "day": "Sat 9:00", "fee": 120}]),
           T("register", "Register for a class.", {"student": str, "class_name": str, "fee": float}, "registered", "money")],
    steps=[call("class_schedule", center="Park District", activity="swim"), call("register", student="{kid}", class_name="Swim Level 2", fee=120.0),
           answer("{kid} is registered for Swim Level 2, Saturdays at 9 ($120).")],
    approvals={"register": "approve"},
    guards={"register": lambda a, p: "over your review limit" if a["fee"] > p["max_purchase_without_review"] else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
