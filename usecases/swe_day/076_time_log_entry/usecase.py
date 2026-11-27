"""Fill in the time log

When:     17:40 (release)
Trigger:  cron: 40 17 * * 1-5
Type:     admin

Nobody likes timesheets; this one is built from calendar and commits.

Run:  python usecases/swe_day/076_time_log_entry/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/076_time_log_entry/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "17:40"
BLOCK = "release"
TRIGGER = "cron: 40 17 * * 1-5"
AUTOMATION = "admin"

USECASE = UseCase(
    id=76,
    domain="swe-" + BLOCK,
    title="Fill in the time log",
    ask="Fill my time log for today.",
    why="Nobody likes timesheets; this one is built from calendar and commits.",
    tools=[TOOL("calendar_today", "Today's meetings.", [{"title": "standup", "mins": 15}, {"title": "arch sync", "mins": 60}]),
           TOOL("commits_today", "Commits today by ticket.", {"PAY-431": 5, "PAY-440": 2}),
           TOOL("log_time", "Log time entries.", "logged", {"entries": list}, "write")],
    plan=[par(call("calendar_today", query="me"), call("commits_today", query="me")),
          call("log_time", entries=[{"ticket": "PAY-431", "hours": 4}, {"ticket": "PAY-440", "hours": 2}, {"ticket": "meetings", "hours": 1.25}]),
          say("Logged 7.25h: PAY-431 4h, PAY-440 2h, meetings 1.25h.")],
    hitl={"log_time": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
