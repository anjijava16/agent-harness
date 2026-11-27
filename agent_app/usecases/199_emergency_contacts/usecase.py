"""Emergency contact sheet

Area: digital
Builds it from contacts and memory, and saves it to the shared family folder.

Run:  python usecases/199_emergency_contacts/usecase.py                  # your preferred framework
      python usecases/199_emergency_contacts/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/199_emergency_contacts/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=199,
    area="digital",
    title="Emergency contact sheet",
    ask="Make an emergency contact sheet for the babysitter.",
    why="Builds it from contacts and memory, and saves it to the shared family folder.",
    tools=[T("contacts", "Contacts by tag.", {"tag": str}, [{"name": "Jordan", "phone": "(312) 555-0101"}, {"name": "Dr. Patel (pediatrician)", "phone": "(312) 555-0199"}]),
           T("file_doc", "Save to a folder.", {"name": str, "folder": str}, "filed", "write")],
    steps=[par(call("contacts", tag="emergency"), recall("plumber")), call("file_doc", name="Emergency contacts.pdf", folder="Family"),
           answer("Emergency sheet saved to Family, with {partner}, the pediatrician and the plumber.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
