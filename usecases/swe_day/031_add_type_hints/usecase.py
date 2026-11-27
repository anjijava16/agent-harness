"""Add type hints to a module

When:     11:45 (coding)
Trigger:  manual
Type:     refactor

Small, verifiable edits checked by a tool.

Run:  python usecases/swe_day/031_add_type_hints/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/031_add_type_hints/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "11:45"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "refactor"

USECASE = UseCase(
    id=31,
    domain="swe-" + BLOCK,
    title="Add type hints to a module",
    ask="Add type hints to payments/fees.py and make mypy pass.",
    why="Small, verifiable edits checked by a tool.",
    tools=[TOOL("run_mypy", "Run mypy.", {"errors": 0}, {"path": str})],
    seed_files={"/repo/payments/fees.py": "def compute_fee(amount):\n    return amount * 0.029\n"},
    plan=[read("/repo/payments/fees.py"),
          edit("/repo/payments/fees.py", "def compute_fee(amount):", "def compute_fee(amount: float) -> float:"),
          call("run_mypy", path="payments/fees.py"),
          say("Typed compute_fee(amount: float) -> float; mypy reports 0 errors.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
