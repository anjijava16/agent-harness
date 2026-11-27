"""Plan tomorrow

When:     18:10 (release)
Trigger:  cron: 10 18 * * 1-5
Type:     planning

Keeps a running plan in long-term memory, so tomorrow's morning run picks it up.

Run:  python usecases/swe_day/079_plan_tomorrow/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/079_plan_tomorrow/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "18:10"
BLOCK = "release"
TRIGGER = "cron: 10 18 * * 1-5"
AUTOMATION = "planning"

USECASE = UseCase(
    id=79,
    domain="swe-" + BLOCK,
    title="Plan tomorrow",
    ask="Plan my tomorrow.",
    why="Keeps a running plan in long-term memory, so tomorrow's morning run picks it up.",
    tools=[TOOL("calendar_tomorrow", "Tomorrow's meetings.", [{"title": "1:1", "at": "11:00"}]),
           TOOL("my_open_tickets", "My open tickets.", ["PAY-440 CSV export (in progress)", "PAY-455 retry dashboard"])],
    long_term_memory=True,
    plan=[par(call("calendar_tomorrow", query="me"), call("my_open_tickets", query="me")),
          todos("Finish PAY-440 CSV export (09:00-11:00)", "1:1 at 11:00", "Start PAY-455"),
          write("/memories/tomorrow.md", "- 09:00 PAY-440 CSV export\n- 11:00 1:1\n- PM PAY-455\n"),
          say("Tomorrow: PAY-440 first thing, 1:1 at 11, then start PAY-455. Saved for the morning run.")],
    expect=[("saved to long-term memory", lambda c: "tomorrow.md" in " ".join(c["store_keys"]))]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
