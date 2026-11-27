"""Generate a SQL migration with rollback

When:     11:00 (coding)
Trigger:  manual
Type:     migration

Every migration gets a matching down migration; applying to prod is not a tool it has.

Run:  python usecases/swe_day/027_sql_migration_with_rollback/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/027_sql_migration_with_rollback/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "11:00"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "migration"

USECASE = UseCase(
    id=27,
    domain="swe-" + BLOCK,
    title="Generate a SQL migration with rollback",
    ask="Write the migration for the idempotency_keys table.",
    why="Every migration gets a matching down migration; applying to prod is not a tool it has.",
    tools=[TOOL("latest_migration", "Latest migration id.", "0042")],
    plan=[call("latest_migration", query="repo"),
          write("/repo/migrations/0043_idempotency_keys.up.sql",
                "CREATE TABLE idempotency_keys (key text PRIMARY KEY, response jsonb NOT NULL, expires_at timestamptz NOT NULL);\n"),
          write("/repo/migrations/0043_idempotency_keys.down.sql", "DROP TABLE idempotency_keys;\n"),
          say("Migration 0043 written with up and down scripts.")],
    expect=[("down migration exists", lambda c: "/repo/migrations/0043_idempotency_keys.down.sql" in c["files"])]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
