"""Flaky test report

When:     07:40 (morning)
Trigger:  cron: 40 7 * * 1-5
Type:     scheduled report

Finds tests that both passed and failed on the same commit and remembers the trend across
days.

Run:  python usecases/swe_day/008_flaky_test_report/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/008_flaky_test_report/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "07:40"
BLOCK = "morning"
TRIGGER = "cron: 40 7 * * 1-5"
AUTOMATION = "scheduled report"

USECASE = UseCase(
    id=8,
    domain="swe-" + BLOCK,
    title="Flaky test report",
    ask="Which tests flaked in the last 24 hours?",
    why="Finds tests that both passed and failed on the same commit and remembers the trend across days.",
    tools=[TOOL("test_outcomes", "Test outcomes by commit.", [{"test": "test_checkout_retry", "pass": 7, "fail": 3, "same_commit": True},
                                                             {"test": "test_refund_flow", "pass": 10, "fail": 0, "same_commit": False}], {"window": str})],
    long_term_memory=True,
    plan=[call("test_outcomes", window="24h"),
          write("/memories/flaky_tests.md", "- 2026-11-26 test_checkout_retry 3/10 flaky\n"),
          say("1 flaky test: test_checkout_retry (3 of 10 runs failed on the same commit). Logged to the flaky-test history.")],
    expect=[("trend saved", lambda c: "/flaky_tests.md" in c["store_keys"])]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
