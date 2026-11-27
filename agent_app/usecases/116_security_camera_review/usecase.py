"""Who came to the door

Area: home
Summarizes doorbell events.

Run:  python usecases/116_security_camera_review/usecase.py                  # your preferred framework
      python usecases/116_security_camera_review/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/116_security_camera_review/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=116,
    area="home",
    title="Who came to the door",
    ask="Who came to the door today?",
    why="Summarizes doorbell events.",
    tools=[T("doorbell_events", "Doorbell events.", {"day": str}, [{"time": "11:02", "what": "UPS delivery"}, {"time": "15:40", "what": "unknown, left after 10s"}])],
    steps=[call("doorbell_events", day="today"),
           answer("UPS delivered at 11:02. Someone you don't know rang at 15:40 and left after 10 seconds. The clip is in the app.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
