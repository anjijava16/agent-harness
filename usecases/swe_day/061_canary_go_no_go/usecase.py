"""Canary go / no-go

When:     15:25 (ops)
Trigger:  webhook: canary_window_complete
Type:     deploy decision

Compares canary and baseline metrics against fixed thresholds and returns a typed verdict.

Run:  python usecases/swe_day/061_canary_go_no_go/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/061_canary_go_no_go/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "15:25"
BLOCK = "ops"
TRIGGER = "webhook: canary_window_complete"
AUTOMATION = "deploy decision"

USECASE = UseCase(
    id=61,
    domain="swe-" + BLOCK,
    title="Canary go / no-go",
    ask="Is the ledger v3.2 canary good to promote?",
    why="Compares canary and baseline metrics against fixed thresholds and returns a typed verdict.",
    tools=[TOOL("canary_compare", "Canary vs baseline metrics.", {"error_rate": [0.004, 0.003], "p99_ms": [410, 380]}, {"service": str})],
    agents_md="# Canary rules\nNo-go if error rate > 1.5x baseline or p99 > 1.2x baseline.\n",
    plan=[call("canary_compare", service="ledger"),
          answer("CanaryVerdict", go=True, reasons=["error rate 1.33x (limit 1.5x)", "p99 1.08x (limit 1.2x)"])],
    output=("CanaryVerdict", {"go": bool, "reasons": list})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
