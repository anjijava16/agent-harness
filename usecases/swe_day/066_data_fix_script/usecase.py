"""One-off data fix script

When:     15:55 (ops)
Trigger:  manual: from ticket
Type:     data fix

Writes the script with a dry run first. The real run changes prod data, so it needs
approval.

Run:  python usecases/swe_day/066_data_fix_script/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/066_data_fix_script/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "15:55"
BLOCK = "ops"
TRIGGER = "manual: from ticket"
AUTOMATION = "data fix"

USECASE = UseCase(
    id=66,
    domain="swe-" + BLOCK,
    title="One-off data fix script",
    ask="Fix the 37 invoices stuck in 'pending' after yesterday's outage.",
    why="Writes the script with a dry run first. The real run changes prod data, so it needs approval.",
    tools=[TOOL("run_sql", "Run SQL against prod.", lambda sql, dry_run: {"rows": 37, "dry_run": dry_run}, {"sql": str, "dry_run": bool}, "write")],
    plan=[write("/scripts/fix_pending_invoices.sql", "UPDATE invoices SET status='open' WHERE status='pending' AND updated_at < now() - interval '1 day';\n"),
          call("run_sql", sql="UPDATE invoices SET status='open' WHERE status='pending'", dry_run=True),
          call("run_sql", sql="UPDATE invoices SET status='open' WHERE status='pending'", dry_run=False),
          say("Dry run matched 37 rows; real run updated 37 invoices to open.")],
    hitl={"run_sql": ["approve", "approve"]}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
