"""Sign up for a 10K

Area: health
Registration is a payment, so it needs approval.

Run:  python usecases/133_race_signup/usecase.py                  # your preferred framework
      python usecases/133_race_signup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/133_race_signup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=133,
    area="health",
    title="Sign up for a 10K",
    ask="Sign me up for the spring 10K.",
    why="Registration is a payment, so it needs approval.",
    tools=[T("race_info", "Race details.", {"race": str}, {"date": "Apr 19", "fee": 55}),
           T("register_race", "Register for a race.", {"race": str, "fee": float}, "registered", "money")],
    steps=[call("race_info", race="Spring 10K"), call("register_race", race="Spring 10K", fee=55.0),
           answer("You're registered for the Spring 10K on April 19 ($55).")],
    approvals={"register_race": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
