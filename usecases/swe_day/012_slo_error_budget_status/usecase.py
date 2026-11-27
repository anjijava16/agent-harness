"""SLO and error budget status

When:     08:05 (morning)
Trigger:  cron: 5 8 * * 1-5
Type:     scheduled check

Simple math done reliably every morning, and a freeze suggestion when budget is low.

Run:  python usecases/swe_day/012_slo_error_budget_status/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/012_slo_error_budget_status/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "08:05"
BLOCK = "morning"
TRIGGER = "cron: 5 8 * * 1-5"
AUTOMATION = "scheduled check"

USECASE = UseCase(
    id=12,
    domain="swe-" + BLOCK,
    title="SLO and error budget status",
    ask="How much error budget do my services have left?",
    why="Simple math done reliably every morning, and a freeze suggestion when budget is low.",
    tools=[TOOL("slo_status", "SLO and remaining error budget.", lambda service: {"payments-api": {"slo": 99.9, "budget_left": 0.18},
                                                                                "ledger": {"slo": 99.95, "budget_left": 0.71}}[service], {"service": str})],
    plan=[par(call("slo_status", service="payments-api"), call("slo_status", service="ledger")),
          say("payments-api has 18% of its monthly error budget left: suggest pausing risky deploys. ledger is fine (71%).")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
