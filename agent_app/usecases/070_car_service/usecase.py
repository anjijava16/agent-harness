"""Book a car service

Area: errands
Checks mileage, finds a slot that fits your calendar, books after approval.

Run:  python usecases/070_car_service/usecase.py                  # your preferred framework
      python usecases/070_car_service/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/070_car_service/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=70,
    area="errands",
    title="Book a car service",
    ask="My car is due for an oil change. Book it.",
    why="Checks mileage, finds a slot that fits your calendar, books after approval.",
    tools=[T("car_status", "Car mileage and service due.", {"car": str}, {"miles": 31200, "oil_due_at": 31000}),
           T("garage_slots", "Garage slots.", {"garage": str}, ["Mon 08:00", "Fri 12:00"]),
           T("book", "Book a slot.", {"garage": str, "slot": str}, "booked", "external")],
    steps=[par(call("car_status", car="main"), call("garage_slots", garage="Quick Lube")),
           call("book", garage="Quick Lube", slot="Mon 08:00"),
           answer("You're 200 miles past due. Booked at Quick Lube for Monday 8:00.")],
    approvals={"book": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
