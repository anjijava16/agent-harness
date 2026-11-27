"""Write unit tests for a function

When:     10:00 (coding)
Trigger:  manual
Type:     test generation

Reads the real source, writes tests next to it, runs them through a tool.

Run:  python usecases/swe_day/023_write_unit_tests/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/023_write_unit_tests/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "10:00"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "test generation"

USECASE = UseCase(
    id=23,
    domain="swe-" + BLOCK,
    title="Write unit tests for a function",
    ask="Write unit tests for round_refund() in payments/refunds.py.",
    why="Reads the real source, writes tests next to it, runs them through a tool.",
    tools=[TOOL("run_tests", "Run pytest on a path.", {"passed": 4, "failed": 0}, {"path": str})],
    seed_files={"/repo/payments/refunds.py": "def round_refund(amount):\n    return round(amount + 1e-9, 2)\n"},
    plan=[read("/repo/payments/refunds.py"),
          write("/repo/tests/test_refunds.py", "from payments.refunds import round_refund\n\ndef test_half_up():\n    assert round_refund(1.005) == 1.01\n"),
          call("run_tests", path="tests/test_refunds.py"),
          say("Added 4 tests for round_refund (including the 1.005 half-up case). All pass.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
