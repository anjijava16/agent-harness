"""My flight is delayed

Area: travel
Pulls rebooking options. Switching flights needs your approval.

Run:  python usecases/087_flight_delay_rebook/usecase.py                  # your preferred framework
      python usecases/087_flight_delay_rebook/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/087_flight_delay_rebook/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=87,
    area="travel",
    title="My flight is delayed",
    ask="My flight is delayed 3 hours. Options?",
    why="Pulls rebooking options. Switching flights needs your approval.",
    tools=[T("flight_status", "Status of a flight.", {"flight": str}, {"delay_min": 185, "reason": "crew"}),
           T("rebook_options", "Alternative flights.", {"flight": str}, [{"flight": "UA 611", "depart": "15:05", "fee": 0}]),
           T("rebook", "Switch to another flight.", {"flight": str}, "rebooked", "external")],
    steps=[par(call("flight_status", flight="UA 455"), call("rebook_options", flight="UA 455")),
           call("rebook", flight="UA 611"),
           answer("UA 455 is 3 hours late. You're now on UA 611 at 15:05, no fee.")],
    approvals={"rebook": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
