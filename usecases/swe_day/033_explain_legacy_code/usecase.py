"""Explain legacy code before changing it

When:     12:05 (coding)
Trigger:  manual
Type:     code understanding

A reader subagent walks the file so the main agent can give a short, accurate explanation.

Run:  python usecases/swe_day/033_explain_legacy_code/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/033_explain_legacy_code/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "12:05"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "code understanding"

USECASE = UseCase(
    id=33,
    domain="swe-" + BLOCK,
    title="Explain legacy code before changing it",
    ask="What does reconcile_ledger() actually do?",
    why="A reader subagent walks the file so the main agent can give a short, accurate explanation.",
    tools=[],
    seed_files={"/repo/ledger/reconcile.py": "def reconcile_ledger(day):\n    # sums debits/credits, writes diff to suspense account if != 0\n    ...\n"},
    subagents=[SUB("code-reader", "Reads and explains code.", [], [say("Sums the day's debits and credits; any difference goes to the suspense account.")])],
    plan=[read("/repo/ledger/reconcile.py"), task("code-reader", "Explain reconcile_ledger in plain English."),
          say("reconcile_ledger(day) totals that day's debits and credits and books any mismatch to the suspense account. It doesn't fix the mismatch.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
