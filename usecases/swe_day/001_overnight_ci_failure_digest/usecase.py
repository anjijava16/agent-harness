"""Overnight CI failure digest

When:     06:30 (morning)
Trigger:  cron: 30 6 * * 1-5
Type:     scheduled digest

Nobody should start the day by scrolling CI pages. A subagent groups failures by cause;
only the summary reaches you.

Run:  python usecases/swe_day/001_overnight_ci_failure_digest/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/001_overnight_ci_failure_digest/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "06:30"
BLOCK = "morning"
TRIGGER = "cron: 30 6 * * 1-5"
AUTOMATION = "scheduled digest"

USECASE = UseCase(
    id=1,
    domain="swe-" + BLOCK,
    title="Overnight CI failure digest",
    ask="Summarize what broke in CI overnight on main and the release branches.",
    why="Nobody should start the day by scrolling CI pages. A subagent groups failures by cause; only the summary reaches you.",
    tools=[TOOL("list_failed_runs", "Failed CI runs in a time window.",
                [{"run": 9912, "branch": "main", "job": "integration", "error": "connection refused :5432"},
                 {"run": 9915, "branch": "main", "job": "integration", "error": "connection refused :5432"},
                 {"run": 9920, "branch": "release/4.2", "job": "lint", "error": "E501 line too long"}], {"since": str})],
    subagents=[SUB("ci-analyst", "Groups CI failures by root cause.", ["list_failed_runs"],
                   [call("list_failed_runs", since="18:00 yesterday"),
                    say("2 integration failures on main share one cause (Postgres not ready). 1 lint failure on release/4.2.")])],
    plan=[task("ci-analyst", "What failed overnight and why?"),
          write("/digests/ci_overnight.md", "- main/integration x2: Postgres service not ready (infra)\n- release/4.2/lint x1: E501\n"),
          say("Overnight CI: 2 main integration failures, same cause (Postgres container not ready). 1 lint error on release/4.2. Digest saved.")],
    expect=[("digest written", lambda c: "/digests/ci_overnight.md" in c["files"])]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
