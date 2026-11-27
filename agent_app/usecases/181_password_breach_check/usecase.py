"""Were any of my accounts breached?

Area: digital
Checks breach data and lists which accounts to change. It never sees passwords.

Run:  python usecases/181_password_breach_check/usecase.py                  # your preferred framework
      python usecases/181_password_breach_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/181_password_breach_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=181,
    area="digital",
    title="Were any of my accounts breached?",
    ask="Check if my email showed up in a data breach.",
    why="Checks breach data and lists which accounts to change. It never sees passwords.",
    tools=[T("breach_check", "Breaches for an email address.", {"email": str}, [{"site": "OldForum", "year": 2024, "data": "email, password hash"}])],
    steps=[call("breach_check", email="sam@example.com"),
           answer("Found in one breach: OldForum (2024). If you reused that password anywhere, change it, and turn on 2FA.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
