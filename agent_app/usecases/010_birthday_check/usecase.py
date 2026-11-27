"""Birthdays coming up

Area: mornings
Checks contacts and offers a card. Sending one is a real purchase, so it needs approval.

Run:  python usecases/010_birthday_check/usecase.py                  # your preferred framework
      python usecases/010_birthday_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/010_birthday_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=10,
    area="mornings",
    title="Birthdays coming up",
    ask="Any birthdays this week?",
    why="Checks contacts and offers a card. Sending one is a real purchase, so it needs approval.",
    tools=[T("birthdays", "Contacts with birthdays in N days.", {"days": int}, [{"name": "Aunt Rosa", "date": "Thursday"}]),
           T("send_ecard", "Send an e-card.", {"to": str, "message": str}, "sent", "external")],
    steps=[call("birthdays", days=7), call("send_ecard", to="Aunt Rosa", message="Happy birthday, Rosa!"),
           answer("Aunt Rosa's birthday is Thursday, and the card is sent with your wording.")],
    approvals={"send_ecard": ("edit", {"message": "Happy birthday Tia Rosa! Can't wait to see you at Thanksgiving."})},
    expect=[("your wording used", lambda c: "Thanksgiving" in c["actions"][0]["args"]["message"])]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
