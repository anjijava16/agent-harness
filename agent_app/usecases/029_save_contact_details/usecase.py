"""Save a new contact from an email

Area: inbox
Extracts details from the email signature and creates the contact.

Run:  python usecases/029_save_contact_details/usecase.py                  # your preferred framework
      python usecases/029_save_contact_details/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/029_save_contact_details/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=29,
    area="inbox",
    title="Save a new contact from an email",
    ask="Save the plumber from that email as a contact.",
    why="Extracts details from the email signature and creates the contact.",
    tools=[T("get_email", "Get an email.", {"id": int}, {"signature": "Marco Diaz, Diaz Plumbing, (312) 555-0142"}),
           T("create_contact", "Create a contact.", {"name": str, "phone": str, "note": str}, "created", "write")],
    steps=[call("get_email", id=41), call("create_contact", name="Marco Diaz", phone="(312) 555-0142", note="Plumber"),
           remember("plumber", "Marco Diaz, (312) 555-0142"),
           answer("Saved Marco Diaz (Diaz Plumbing) with his number.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
