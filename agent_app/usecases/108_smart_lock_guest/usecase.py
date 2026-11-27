"""Guest access for the dog walker

Area: home
Time-limited codes are allowed. Permanent codes are blocked.

Run:  python usecases/108_smart_lock_guest/usecase.py                  # your preferred framework
      python usecases/108_smart_lock_guest/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/108_smart_lock_guest/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=108,
    area="home",
    title="Guest access for the dog walker",
    ask="Give the dog walker a door code for weekdays at noon.",
    why="Time-limited codes are allowed. Permanent codes are blocked.",
    tools=[T("create_door_code", "Create a door code.", {"name": str, "schedule": str, "permanent": bool}, {"code": "4821"}, "write")],
    steps=[call("create_door_code", name="dog walker", schedule="Mon-Fri 11:45-12:45", permanent=False),
           answer("Code created for the dog walker, weekdays 11:45-12:45 only.")],
    approvals={"create_door_code": "approve"},
    guards={"create_door_code": lambda a, p: "permanent codes are not allowed" if a["permanent"] else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
