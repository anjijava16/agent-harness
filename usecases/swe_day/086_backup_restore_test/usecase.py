"""Backup restore test

When:     21:30 (night)
Trigger:  cron: 30 21 * * 6
Type:     DR

A backup you haven't restored is a guess. The restore target is checked so it never points
at prod.

Run:  python usecases/swe_day/086_backup_restore_test/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/086_backup_restore_test/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "21:30"
BLOCK = "night"
TRIGGER = "cron: 30 21 * * 6"
AUTOMATION = "DR"

USECASE = UseCase(
    id=86,
    domain="swe-" + BLOCK,
    title="Backup restore test",
    ask="Restore last night's ledger backup to a scratch DB and verify it.",
    why="A backup you haven't restored is a guess. The restore target is checked so it never points at prod.",
    tools=[TOOL("restore_backup", "Restore a backup to a target DB.", "restored", {"backup": str, "target": str}, "write"),
           TOOL("row_counts", "Row counts in a DB.", {"entries": 48211002, "accounts": 91233}, {"db": str})],
    plan=[call("restore_backup", backup="ledger-2026-11-25", target="ledger-prod"),
          call("restore_backup", backup="ledger-2026-11-25", target="ledger-scratch"),
          call("row_counts", db="ledger-scratch"),
          say("Restore to scratch OK: 48.2M entries, 91k accounts. The attempt to target prod was blocked.")],
    guard={"restore_backup": lambda a: "restore target must not be prod" if "prod" in a["target"] else None}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
