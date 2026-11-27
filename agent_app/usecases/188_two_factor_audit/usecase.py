"""Which accounts lack 2FA

Area: digital
Checks the password manager's security report.

Run:  python usecases/188_two_factor_audit/usecase.py                  # your preferred framework
      python usecases/188_two_factor_audit/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/188_two_factor_audit/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=188,
    area="digital",
    title="Which accounts lack 2FA",
    ask="Which of my important accounts don't have 2FA?",
    why="Checks the password manager's security report.",
    tools=[T("security_report", "Password manager security report.", {"vault": str}, {"no_2fa": ["bank", "email backup"], "reused": 3})],
    steps=[call("security_report", vault="personal"),
           answer("Your bank and backup email have no 2FA; set those up first. 3 passwords are also reused.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
