"""Unsubscribe from junk

Area: inbox
Uses open-rate data. You reject one unsubscribe you want to keep.

Run:  python usecases/023_unsubscribe_cleanup/usecase.py                  # your preferred framework
      python usecases/023_unsubscribe_cleanup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/023_unsubscribe_cleanup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=23,
    area="inbox",
    title="Unsubscribe from junk",
    ask="Unsubscribe me from newsletters I never open.",
    why="Uses open-rate data. You reject one unsubscribe you want to keep.",
    tools=[T("never_opened", "Senders you haven't opened in 90 days.", {"days": int}, ["dealsdaily", "crypto-weekly", "local-library"]),
           T("unsubscribe", "Unsubscribe from a sender.", {"sender": str}, "unsubscribed", "external")],
    steps=[call("never_opened", days=90),
           par(call("unsubscribe", sender="dealsdaily"), call("unsubscribe", sender="crypto-weekly"), call("unsubscribe", sender="local-library")),
           answer("Unsubscribed from 2. Kept local-library as you asked.")],
    approvals={"unsubscribe": ["approve", "approve", "reject"]},
    expect=[("library kept", lambda c: all(a["args"]["sender"] != "local-library" for a in c["actions"]))]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
