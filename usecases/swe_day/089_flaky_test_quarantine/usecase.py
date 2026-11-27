"""Quarantine flaky tests

When:     22:30 (night)
Trigger:  cron: 30 22 * * *
Type:     CI hygiene

Edits the quarantine list file and opens a PR. People decide whether to fix or delete.

Run:  python usecases/swe_day/089_flaky_test_quarantine/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/089_flaky_test_quarantine/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "22:30"
BLOCK = "night"
TRIGGER = "cron: 30 22 * * *"
AUTOMATION = "CI hygiene"

USECASE = UseCase(
    id=89,
    domain="swe-" + BLOCK,
    title="Quarantine flaky tests",
    ask="Quarantine tests that flaked more than 3 times this week.",
    why="Edits the quarantine list file and opens a PR. People decide whether to fix or delete.",
    tools=[TOOL("flake_counts", "Flake counts this week.", {"test_webhook_retry": 5, "test_refund_total": 1}),
           TOOL("open_pr", "Open a PR.", "opened", {"title": str, "branch": str}, "external")],
    seed_files={"/repo/tests/quarantine.txt": "test_old_thing\n"},
    plan=[call("flake_counts", query="week"), read("/repo/tests/quarantine.txt"),
          edit("/repo/tests/quarantine.txt", "test_old_thing\n", "test_old_thing\ntest_webhook_retry\n"),
          call("open_pr", title="Quarantine test_webhook_retry (5 flakes this week)", branch="ci/quarantine"),
          say("Quarantined test_webhook_retry (5 flakes) and opened a PR.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
