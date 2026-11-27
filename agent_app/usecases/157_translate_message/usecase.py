"""Translate a message

Area: work
Translates and sends after approval.

Run:  python usecases/157_translate_message/usecase.py                  # your preferred framework
      python usecases/157_translate_message/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/157_translate_message/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=157,
    area="work",
    title="Translate a message",
    ask="Translate my reply to the Madrid team into Spanish.",
    why="Translates and sends after approval.",
    tools=[T("translate", "Translate text.", {"text": str, "to_lang": str}, "Gracias, revisaré la propuesta el jueves."),
           T("send_email", "Send an email.", {"to": str, "body": str}, "sent", "external")],
    steps=[call("translate", text="Thanks, I'll review the proposal on Thursday.", to_lang="es"),
           call("send_email", to="madrid-team", body="Gracias, revisaré la propuesta el jueves."),
           answer("Translated and sent to the Madrid team.")],
    approvals={"send_email": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
