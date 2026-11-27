"""Standup notes from yesterday's activity

When:     07:20 (morning)
Trigger:  cron: 20 7 * * 1-5
Type:     auto-draft

Builds yesterday/today/blockers from commits and tickets, in the team's format from
AGENTS.md.

Run:  python usecases/swe_day/006_standup_notes_from_activity/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/006_standup_notes_from_activity/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "07:20"
BLOCK = "morning"
TRIGGER = "cron: 20 7 * * 1-5"
AUTOMATION = "auto-draft"

USECASE = UseCase(
    id=6,
    domain="swe-" + BLOCK,
    title="Standup notes from yesterday's activity",
    ask="Draft my standup update.",
    why="Builds yesterday/today/blockers from commits and tickets, in the team's format from AGENTS.md.",
    tools=[TOOL("my_commits", "My commits since a time.", ["fix: retry ledger writes on 409", "test: cover refund rounding"], {"since": str}),
           TOOL("my_tickets", "My tickets by status.", {"in_progress": ["PAY-431 idempotency keys"], "blocked": ["PAY-428 waiting on infra"]})],
    agents_md="# Standup format\nYesterday: ...\nToday: ...\nBlockers: ...\nMax 3 lines each.\n",
    plan=[par(call("my_commits", since="yesterday"), call("my_tickets", query="me")),
          say("Yesterday: retried ledger writes on 409, covered refund rounding. Today: PAY-431 idempotency keys. Blockers: PAY-428 waiting on infra.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
