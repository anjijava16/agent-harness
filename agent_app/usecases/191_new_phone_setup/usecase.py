"""New phone checklist

Area: digital
Builds a checklist from the apps and 2FA you saved in memory.

Run:  python usecases/191_new_phone_setup/usecase.py                  # your preferred framework
      python usecases/191_new_phone_setup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/191_new_phone_setup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=191,
    area="digital",
    title="New phone checklist",
    ask="I got a new phone. What do I need to move over?",
    why="Builds a checklist from the apps and 2FA you saved in memory.",
    tools=[T("app_list", "Apps on the old phone.", {"device": str}, ["bank", "authenticator", "transit", "messages"])],
    steps=[par(call("app_list", device="old phone"), recall("2fa")),
           answer("Move the authenticator first, before you wipe the old phone. Then the bank app, then messages and transit.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
