"""Nightly full test run and coverage

When:     19:30 (night)
Trigger:  cron: 30 19 * * *
Type:     testing

Catches slow coverage drift that per-PR checks miss.

Run:  python usecases/swe_day/082_nightly_test_and_coverage/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/082_nightly_test_and_coverage/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "19:30"
BLOCK = "night"
TRIGGER = "cron: 30 19 * * *"
AUTOMATION = "testing"

USECASE = UseCase(
    id=82,
    domain="swe-" + BLOCK,
    title="Nightly full test run and coverage",
    ask="Run the full suite and report coverage changes.",
    why="Catches slow coverage drift that per-PR checks miss.",
    tools=[TOOL("full_test_run", "Full test suite with coverage.", {"passed": 1420, "failed": 0, "coverage": 81.2, "previous": 83.0})],
    plan=[call("full_test_run", query="all"),
          answer("NightlyTests", passed=1420, failed=0, coverage=81.2, coverage_delta=-1.8)],
    output=("NightlyTests", {"passed": int, "failed": int, "coverage": float, "coverage_delta": float})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
