"""Pharmacy pickup check

Area: errands
Checks the pharmacy status. No medical advice, just logistics.

Run:  python usecases/065_pharmacy_pickup/usecase.py                  # your preferred framework
      python usecases/065_pharmacy_pickup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/065_pharmacy_pickup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=65,
    area="errands",
    title="Pharmacy pickup check",
    ask="Is my prescription ready?",
    why="Checks the pharmacy status. No medical advice, just logistics.",
    tools=[T("rx_status", "Prescription status.", {"pharmacy": str}, {"ready": True, "pickup_by": "Saturday"})],
    steps=[call("rx_status", pharmacy="neighborhood"), answer("It's ready. Pick it up by Saturday.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
