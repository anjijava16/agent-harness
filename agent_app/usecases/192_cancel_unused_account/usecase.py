"""Close an old account

Area: digital
Deleting an account can't be undone, so it needs approval.

Run:  python usecases/192_cancel_unused_account/usecase.py                  # your preferred framework
      python usecases/192_cancel_unused_account/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/192_cancel_unused_account/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=192,
    area="digital",
    title="Close an old account",
    ask="Delete my OldForum account.",
    why="Deleting an account can't be undone, so it needs approval.",
    tools=[T("account_status", "Account status.", {"site": str}, {"exists": True, "last_login": "2023"}),
           T("delete_account", "Request account deletion.", {"site": str}, "requested", "external")],
    steps=[call("account_status", site="OldForum"), call("delete_account", site="OldForum"),
           answer("Deletion requested for OldForum. Your last login there was in 2023.")],
    approvals={"delete_account": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
