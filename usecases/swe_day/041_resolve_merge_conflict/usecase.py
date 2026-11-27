"""Resolve a merge conflict

When:     12:50 (review)
Trigger:  manual
Type:     git

Reads both sides of the conflict, keeps both intents, reruns tests.

Run:  python usecases/swe_day/041_resolve_merge_conflict/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/041_resolve_merge_conflict/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "12:50"
BLOCK = "review"
TRIGGER = "manual"
AUTOMATION = "git"

USECASE = UseCase(
    id=41,
    domain="swe-" + BLOCK,
    title="Resolve a merge conflict",
    ask="Rebase my branch on main; there's a conflict in fees.py.",
    why="Reads both sides of the conflict, keeps both intents, reruns tests.",
    tools=[TOOL("run_tests", "Run tests.", {"passed": 214, "failed": 0}, {"path": str})],
    seed_files={"/repo/payments/fees.py": "<<<<<<< HEAD\nRATE = 0.029\n=======\nRATE = 0.029\nFIXED = 0.30\n>>>>>>> feature\n"},
    plan=[read("/repo/payments/fees.py"),
          write("/repo/payments/fees.py", "RATE = 0.029\nFIXED = 0.30\n"),
          call("run_tests", path="."),
          say("Kept main's RATE and your FIXED fee. Conflict markers removed, tests pass.")],
    expect=[("no conflict markers", lambda c: "<<<<<<<" not in c["files"]["/repo/payments/fees.py"])]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
