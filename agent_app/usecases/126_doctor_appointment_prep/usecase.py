"""Prep for a doctor's appointment

Area: health
Pulls together the questions you saved and the logistics. It gives no medical advice.

Run:  python usecases/126_doctor_appointment_prep/usecase.py                  # your preferred framework
      python usecases/126_doctor_appointment_prep/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/126_doctor_appointment_prep/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=126,
    area="health",
    title="Prep for a doctor's appointment",
    ask="Help me prepare for my checkup on Friday.",
    why="Pulls together the questions you saved and the logistics. It gives no medical advice.",
    tools=[T("appointment", "Appointment details.", {"day": str}, {"clinic": "Northside Clinic", "time": "08:40", "bring": "insurance card"})],
    steps=[par(call("appointment", day="Fri"), recall("doctor_questions")),
           answer("Friday 08:40 at Northside Clinic. Bring your insurance card. Your saved questions are in the notes.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
