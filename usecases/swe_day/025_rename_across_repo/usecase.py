"""Rename a function across the repo

When:     10:30 (coding)
Trigger:  manual
Type:     refactor

grep-then-edit over real files, then run the tests.

Run:  python usecases/swe_day/025_rename_across_repo/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/025_rename_across_repo/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "10:30"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "refactor"

USECASE = UseCase(
    id=25,
    domain="swe-" + BLOCK,
    title="Rename a function across the repo",
    ask="Rename calc_fee to compute_fee everywhere.",
    why="grep-then-edit over real files, then run the tests.",
    tools=[TOOL("run_tests", "Run the test suite.", {"passed": 212, "failed": 0}, {"path": str})],
    seed_files={"/repo/payments/fees.py": "def calc_fee(amount):\n    return amount * 0.029\n",
                "/repo/payments/api.py": "from payments.fees import calc_fee\n\nfee = calc_fee(100)\n"},
    plan=[call("grep", pattern="calc_fee", path="/repo"),
          edit("/repo/payments/fees.py", "def calc_fee", "def compute_fee"),
          edit("/repo/payments/api.py", "from payments.fees import calc_fee\n\nfee = calc_fee(100)", "from payments.fees import compute_fee\n\nfee = compute_fee(100)"),
          call("run_tests", path="."),
          say("Renamed calc_fee to compute_fee in 2 files; 212 tests pass.")],
    expect=[("no calc_fee left", lambda c: all("calc_fee" not in v for k, v in c["files"].items() if k.startswith("/repo/")))]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
