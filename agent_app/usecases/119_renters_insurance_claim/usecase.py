"""Start an insurance claim

Area: home
Gathers the photos and the plumber's notes and files the claim after you edit it.

Run:  python usecases/119_renters_insurance_claim/usecase.py                  # your preferred framework
      python usecases/119_renters_insurance_claim/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/119_renters_insurance_claim/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=119,
    area="home",
    title="Start an insurance claim",
    ask="The leak damaged the cabinet. Start a claim.",
    why="Gathers the photos and the plumber's notes and files the claim after you edit it.",
    tools=[T("photos", "Photos by date.", {"date": str}, {"count": 6}),
           T("file_claim", "File an insurance claim.", {"description": str, "photos": int}, {"claim": "C-2281"}, "external")],
    steps=[call("photos", date="today"), call("file_claim", description="Water damage from sink leak", photos=6),
           answer("Claim C-2281 filed with 6 photos.")],
    approvals={"file_claim": ("edit", {"description": "Water damage to the kitchen sink cabinet from a supply-line leak. Plumber repaired it on Thursday."})}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
