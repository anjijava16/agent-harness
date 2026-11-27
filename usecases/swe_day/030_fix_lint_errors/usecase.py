"""Fix a batch of lint errors

When:     11:35 (coding)
Trigger:  manual
Type:     cleanup

Tedious work an agent does well; it edits files and reruns the linter.

Run:  python usecases/swe_day/030_fix_lint_errors/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/030_fix_lint_errors/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "11:35"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "cleanup"

USECASE = UseCase(
    id=30,
    domain="swe-" + BLOCK,
    title="Fix a batch of lint errors",
    ask="Fix the lint errors in payments/.",
    why="Tedious work an agent does well; it edits files and reruns the linter.",
    tools=[TOOL("run_linter", "Run the linter.", lambda path: [] , {"path": str})],
    seed_files={"/repo/payments/util.py": "import os, sys\ndef f( x ):\n    return x\n"},
    plan=[read("/repo/payments/util.py"),
          edit("/repo/payments/util.py", "import os, sys\ndef f( x ):\n    return x\n", "def f(x):\n    return x\n"),
          call("run_linter", path="payments/"),
          say("Fixed unused imports and spacing in payments/util.py; linter is clean.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
