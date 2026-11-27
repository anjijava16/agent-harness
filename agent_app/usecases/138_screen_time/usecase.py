"""Screen time check

Area: health
Reads screen-time stats and sets one app limit after approval.

Run:  python usecases/138_screen_time/usecase.py                  # your preferred framework
      python usecases/138_screen_time/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/138_screen_time/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=138,
    area="health",
    title="Screen time check",
    ask="How much time did I spend on my phone this week?",
    why="Reads screen-time stats and sets one app limit after approval.",
    tools=[T("screen_time", "Screen time by app.", {"days": int}, {"total_h": 21, "top": {"video": 8, "social": 6}}),
           T("set_app_limit", "Set a daily app limit.", {"app_category": str, "minutes": int}, "set", "write")],
    steps=[call("screen_time", days=7), call("set_app_limit", app_category="video", minutes=45),
           answer("21 hours this week, 8 of them on video apps. A 45-minute daily limit is now set for video.")],
    approvals={"set_app_limit": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
