"""Refill a prescription

Area: health
Requests a refill from the pharmacy after approval. Logistics only.

Run:  python usecases/131_prescription_refill/usecase.py                  # your preferred framework
      python usecases/131_prescription_refill/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/131_prescription_refill/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=131,
    area="health",
    title="Refill a prescription",
    ask="Refill my usual prescription.",
    why="Requests a refill from the pharmacy after approval. Logistics only.",
    tools=[T("refills_left", "Refills remaining.", {"rx": str}, 2),
           T("request_refill", "Request a refill.", {"rx": str, "pharmacy": str}, "requested", "external")],
    steps=[call("refills_left", rx="usual"), call("request_refill", rx="usual", pharmacy="neighborhood"),
           answer("Refill requested; 2 refills left. I'll tell you when it's ready.")],
    approvals={"request_refill": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
