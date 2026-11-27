"""Get the plumber in

Area: home
Uses the plumber you saved and texts him after approval.

Run:  python usecases/110_plumber_quote/usecase.py                  # your preferred framework
      python usecases/110_plumber_quote/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/110_plumber_quote/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=110,
    area="home",
    title="Get the plumber in",
    ask="The kitchen sink is leaking. Get the plumber.",
    why="Uses the plumber you saved and texts him after approval.",
    tools=[T("send_sms", "Send a text.", {"to": str, "text": str}, "sent", "external")],
    steps=[recall("plumber"), call("send_sms", to="Marco Diaz", text="Hi Marco, Sam here. Kitchen sink leak. Any time this week?"),
           answer("Texted Marco Diaz about the leak.")],
    approvals={"send_sms": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
