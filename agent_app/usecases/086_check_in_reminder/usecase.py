"""Flight check-in

Area: travel
Checks in when the window opens and asks for your seat preference.

Run:  python usecases/086_check_in_reminder/usecase.py                  # your preferred framework
      python usecases/086_check_in_reminder/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/086_check_in_reminder/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=86,
    area="travel",
    title="Flight check-in",
    ask="Check me in for tomorrow's flight.",
    why="Checks in when the window opens and asks for your seat preference.",
    tools=[T("check_in", "Check in for a flight.", {"flight": str, "seat": str}, {"boarding_pass": "sent to wallet", "seat": "18C"}, "external")],
    steps=[call("check_in", flight="UA 455", seat="{seat_preference}"),
           answer("Checked in, seat 18C ({seat_preference}). The boarding pass is in your wallet.")],
    approvals={"check_in": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
