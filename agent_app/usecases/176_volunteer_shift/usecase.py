"""Sign up to volunteer

Area: learning
Signing up commits your time, so it needs approval.

Run:  python usecases/176_volunteer_shift/usecase.py                  # your preferred framework
      python usecases/176_volunteer_shift/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/176_volunteer_shift/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=176,
    area="learning",
    title="Sign up to volunteer",
    ask="Find a volunteer shift this month and sign me up.",
    why="Signing up commits your time, so it needs approval.",
    tools=[T("volunteer_shifts", "Open volunteer shifts.", {"city": str}, [{"org": "Food Depository", "when": "Sat Dec 13 9-12"}]),
           T("sign_up", "Sign up for a shift.", {"org": str, "when": str}, "signed up", "external")],
    steps=[call("volunteer_shifts", city="{home_city}"), call("sign_up", org="Food Depository", when="Sat Dec 13 9-12"),
           answer("You're signed up at the Food Depository, Saturday Dec 13, 9-12.")],
    approvals={"sign_up": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
