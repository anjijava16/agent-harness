"""Vet appointment for the dog

Area: home
Checks the vaccine record and books after approval.

Run:  python usecases/103_vet_appointment/usecase.py                  # your preferred framework
      python usecases/103_vet_appointment/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/103_vet_appointment/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=103,
    area="home",
    title="Vet appointment for the dog",
    ask="Biscuit is due for vaccines. Book the vet.",
    why="Checks the vaccine record and books after approval.",
    tools=[T("pet_records", "Pet vaccine records.", {"pet": str}, {"rabies_due": "Dec 2"}),
           T("vet_slots", "Vet slots.", {"clinic": str}, ["Sat 10:30", "Mon 17:00"]),
           T("book_vet", "Book a vet slot.", {"clinic": str, "slot": str, "pet": str}, "booked", "external")],
    steps=[par(call("pet_records", pet="{dog}"), call("vet_slots", clinic="Lakeview Vet")),
           call("book_vet", clinic="Lakeview Vet", slot="Sat 10:30", pet="{dog}"),
           answer("{dog}'s rabies shot is due Dec 2. Booked at Lakeview Vet for Saturday 10:30.")],
    approvals={"book_vet": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
