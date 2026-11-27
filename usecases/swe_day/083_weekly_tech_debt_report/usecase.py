"""Weekly tech-debt report

When:     20:00 (night)
Trigger:  cron: 0 20 * * 5
Type:     reporting

Counts TODOs, deprecated calls and big files; writes a report the team skims on Monday.

Run:  python usecases/swe_day/083_weekly_tech_debt_report/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/083_weekly_tech_debt_report/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "20:00"
BLOCK = "night"
TRIGGER = "cron: 0 20 * * 5"
AUTOMATION = "reporting"

USECASE = UseCase(
    id=83,
    domain="swe-" + BLOCK,
    title="Weekly tech-debt report",
    ask="Build the weekly tech-debt report.",
    why="Counts TODOs, deprecated calls and big files; writes a report the team skims on Monday.",
    tools=[TOOL("count_todos", "TODO/FIXME count by dir.", {"payments": 41, "ledger": 12}),
           TOOL("deprecated_usage", "Deprecated API usages.", {"datetime.utcnow": 0, "pydantic.v1": 7}),
           TOOL("largest_files", "Largest source files.", [{"path": "ledger/reconcile.py", "lines": 1840}])],
    plan=[par(call("count_todos", query="repo"), call("deprecated_usage", query="repo"), call("largest_files", query="repo")),
          write("/reports/tech-debt-weekly.md", "TODOs: 53. pydantic.v1 imports: 7. Largest: ledger/reconcile.py (1840 lines).\n"),
          say("Tech-debt report written: 53 TODOs, 7 pydantic.v1 imports, reconcile.py still 1840 lines.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
