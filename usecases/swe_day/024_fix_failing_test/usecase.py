"""Fix a failing test

When:     10:15 (coding)
Trigger:  manual
Type:     bug fix

Read failure, read code, make the smallest edit, rerun.

Run:  python usecases/swe_day/024_fix_failing_test/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/024_fix_failing_test/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "10:15"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "bug fix"

USECASE = UseCase(
    id=24,
    domain="swe-" + BLOCK,
    title="Fix a failing test",
    ask="test_refund_total fails. Fix it.",
    why="Read failure, read code, make the smallest edit, rerun.",
    tools=[TOOL("run_tests", "Run pytest.", lambda path: {"passed": 1, "failed": 0}, {"path": str}),
           TOOL("last_failure", "Last failure output for a test.", "AssertionError: 99.99 != 100.0 (floor used instead of round)", {"test": str})],
    seed_files={"/repo/payments/totals.py": "import math\n\ndef refund_total(x):\n    return math.floor(x * 100) / 100\n"},
    plan=[call("last_failure", test="test_refund_total"), read("/repo/payments/totals.py"),
          edit("/repo/payments/totals.py", "return math.floor(x * 100) / 100", "return round(x, 2)"),
          call("run_tests", path="tests/test_totals.py"),
          say("refund_total used floor() and lost a cent; switched to round(x, 2). Test passes.")],
    expect=[("source fixed", lambda c: "round(x, 2)" in c["files"]["/repo/payments/totals.py"])]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
