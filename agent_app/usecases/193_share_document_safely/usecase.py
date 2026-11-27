"""Share a document safely

Area: digital
Creates a link that expires. Public links that never expire are blocked.

Run:  python usecases/193_share_document_safely/usecase.py                  # your preferred framework
      python usecases/193_share_document_safely/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/193_share_document_safely/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=193,
    area="digital",
    title="Share a document safely",
    ask="Share my lease with the new landlord.",
    why="Creates a link that expires. Public links that never expire are blocked.",
    tools=[T("share_link", "Create a share link.", {"doc": str, "expires_days": int}, {"link": "https://share.example/abc"}, "external")],
    steps=[call("share_link", doc="Lease 2026.pdf", expires_days=0), call("share_link", doc="Lease 2026.pdf", expires_days=7),
           answer("Shared with a link that expires in 7 days. I don't create links that never expire.")],
    approvals={"share_link": "approve"},
    guards={"share_link": lambda a, p: "links must expire" if a["expires_days"] <= 0 else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
