"""Schedule a donation pickup

Area: errands
Books a charity pickup after approval.

Run:  python usecases/078_donate_clothes/usecase.py                  # your preferred framework
      python usecases/078_donate_clothes/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/078_donate_clothes/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=78,
    area="errands",
    title="Schedule a donation pickup",
    ask="Schedule a pickup for two bags of clothes.",
    why="Books a charity pickup after approval.",
    tools=[T("pickup_slots", "Donation pickup slots.", {"charity": str}, ["Tue AM", "Thu PM"]),
           T("schedule_pickup", "Book a pickup.", {"charity": str, "slot": str, "bags": int}, "scheduled", "external")],
    steps=[call("pickup_slots", charity="Goodwill"), call("schedule_pickup", charity="Goodwill", slot="Tue AM", bags=2),
           answer("Goodwill pickup is booked for Tuesday morning, 2 bags.")],
    approvals={"schedule_pickup": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
