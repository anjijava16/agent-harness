"""Book a dental cleaning

Area: health
Checks the history and books after approval.

Run:  python usecases/136_dentist_cleaning/usecase.py                  # your preferred framework
      python usecases/136_dentist_cleaning/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/136_dentist_cleaning/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=136,
    area="health",
    title="Book a dental cleaning",
    ask="When was my last cleaning? Book the next one.",
    why="Checks the history and books after approval.",
    tools=[T("visit_history", "Visit history.", {"provider": str}, {"last": "May 2026"}),
           T("provider_slots", "Open slots.", {"provider": str}, ["Dec 3 9:00"]),
           T("rebook", "Book an appointment.", {"provider": str, "slot": str}, "booked", "external")],
    steps=[par(call("visit_history", provider="dentist"), call("provider_slots", provider="dentist")),
           call("rebook", provider="dentist", slot="Dec 3 9:00"),
           answer("Your last cleaning was in May. The next one is booked for Dec 3 at 9:00.")],
    approvals={"rebook": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
