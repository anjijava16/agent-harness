"""Voicemails to text

Area: inbox
Transcribes them and flags the one that needs a call back.

Run:  python usecases/034_voicemail_transcribe/usecase.py                  # your preferred framework
      python usecases/034_voicemail_transcribe/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/034_voicemail_transcribe/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=34,
    area="inbox",
    title="Voicemails to text",
    ask="What are my voicemails about?",
    why="Transcribes them and flags the one that needs a call back.",
    tools=[T("voicemails", "Transcribed voicemails.", {"days": int}, [{"from": "dentist office", "text": "Confirming 1pm"}, {"from": "unknown", "text": "Car warranty"}])],
    steps=[call("voicemails", days=2),
           answer("The dentist confirmed 1pm. The other one is a car warranty robocall, so ignore it.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
