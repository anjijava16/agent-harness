"""Meeting across time zones

Area: inbox
Checks both time zones and suggests sane hours for both of you.

Run:  python usecases/033_time_zone_meeting/usecase.py                  # your preferred framework
      python usecases/033_time_zone_meeting/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/033_time_zone_meeting/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=33,
    area="inbox",
    title="Meeting across time zones",
    ask="Find a time for a call with my cousin in Madrid.",
    why="Checks both time zones and suggests sane hours for both of you.",
    tools=[T("tz_overlap", "Overlap of waking hours.", {"tz_a": str, "tz_b": str}, ["08:00-10:00 your time = 15:00-17:00 Madrid"])],
    steps=[call("tz_overlap", tz_a="{timezone}", tz_b="Europe/Madrid"),
           answer("Best window: 8 to 10am your time, which is 3 to 5pm in Madrid.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
