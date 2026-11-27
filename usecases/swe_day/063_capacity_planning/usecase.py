"""Capacity planning forecast

When:     15:40 (ops)
Trigger:  cron: 0 15 1 * *
Type:     forecasting

Monthly; fits a trend to real usage and gives a date.

Run:  python usecases/swe_day/063_capacity_planning/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/063_capacity_planning/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "15:40"
BLOCK = "ops"
TRIGGER = "cron: 0 15 1 * *"
AUTOMATION = "forecasting"

USECASE = UseCase(
    id=63,
    domain="swe-" + BLOCK,
    title="Capacity planning forecast",
    ask="When will the ledger DB run out of disk?",
    why="Monthly; fits a trend to real usage and gives a date.",
    tools=[TOOL("disk_history", "Disk usage history (GB per month).", [610, 640, 672, 705, 739], {"db": str}),
           TOOL("disk_size", "Disk size in GB.", 1000, {"db": str})],
    plan=[par(call("disk_history", db="ledger"), call("disk_size", db="ledger")),
          answer("Forecast", growth_gb_per_month=32, months_left=8, action="Plan storage increase or archive in Q2")],
    output=("Forecast", {"growth_gb_per_month": int, "months_left": int, "action": str})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
