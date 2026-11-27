"""Request time off

Area: work
Checks the balance and team calendar, then submits after approval.

Run:  python usecases/150_pto_request/usecase.py                  # your preferred framework
      python usecases/150_pto_request/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/150_pto_request/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=150,
    area="work",
    title="Request time off",
    ask="Request PTO for April 3-13.",
    why="Checks the balance and team calendar, then submits after approval.",
    tools=[T("pto_balance", "PTO balance.", {"user": str}, {"days": 14}),
           T("team_out", "Teammates out on dates.", {"dates": str}, ["Lee Apr 10-11"]),
           T("submit_pto", "Submit a PTO request.", {"dates": str}, "submitted", "external")],
    steps=[par(call("pto_balance", user="me"), call("team_out", dates="Apr 3-13")), call("submit_pto", dates="Apr 3-13"),
           answer("PTO requested for April 3-13. That's 7 working days, and you have 14. Lee is out the 10th and 11th, so arrange cover.")],
    approvals={"submit_pto": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
