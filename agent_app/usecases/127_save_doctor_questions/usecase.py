"""Save questions for the doctor

Area: health
Saved to memory for the appointment prep task.

Run:  python usecases/127_save_doctor_questions/usecase.py                  # your preferred framework
      python usecases/127_save_doctor_questions/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/127_save_doctor_questions/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=127,
    area="health",
    title="Save questions for the doctor",
    ask="Note for my checkup: ask about knee pain when running.",
    why="Saved to memory for the appointment prep task.",
    tools=[],
    steps=[remember("doctor_questions", "knee pain when running"), answer("Saved for Friday's checkup.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
