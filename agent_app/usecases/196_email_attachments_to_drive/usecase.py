"""Save email attachments

Area: digital
Moves attachments into the right folder.

Run:  python usecases/196_email_attachments_to_drive/usecase.py                  # your preferred framework
      python usecases/196_email_attachments_to_drive/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/196_email_attachments_to_drive/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=196,
    area="digital",
    title="Save email attachments",
    ask="Save all the school PDFs from email to the Maya folder.",
    why="Moves attachments into the right folder.",
    tools=[T("attachments", "Email attachments by sender.", {"sender": str}, ["field_trip.pdf", "lunch_menu.pdf"]),
           T("file_doc", "Save to a folder.", {"name": str, "folder": str}, "filed", "write")],
    steps=[call("attachments", sender="school"),
           par(call("file_doc", name="field_trip.pdf", folder="{kid}/School"), call("file_doc", name="lunch_menu.pdf", folder="{kid}/School")),
           answer("2 PDFs saved to {kid}/School.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
