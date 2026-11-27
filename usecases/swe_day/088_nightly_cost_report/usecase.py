"""Nightly cost report

When:     22:15 (night)
Trigger:  cron: 15 22 * * *
Type:     FinOps

Structured output feeds a dashboard; the agent just does the gathering.

Run:  python usecases/swe_day/088_nightly_cost_report/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/088_nightly_cost_report/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "22:15"
BLOCK = "night"
TRIGGER = "cron: 15 22 * * *"
AUTOMATION = "FinOps"

USECASE = UseCase(
    id=88,
    domain="swe-" + BLOCK,
    title="Nightly cost report",
    ask="Summarise today's cloud spend by service.",
    why="Structured output feeds a dashboard; the agent just does the gathering.",
    tools=[TOOL("cost_by_service", "Spend by service today.", {"payments-api": 410, "ledger": 980, "checkout": 220})],
    plan=[call("cost_by_service", query="today"),
          answer("CostReport", total=1610, top_service="ledger", by_service={"payments-api": 410, "ledger": 980, "checkout": 220})],
    output=("CostReport", {"total": int, "top_service": str, "by_service": dict})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
