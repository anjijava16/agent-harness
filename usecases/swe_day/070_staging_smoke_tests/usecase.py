"""Smoke tests on staging

When:     16:30 (release)
Trigger:  webhook: deploy.succeeded(staging)
Type:     testing

Runs the suites in parallel and reports only what matters.

Run:  python usecases/swe_day/070_staging_smoke_tests/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/070_staging_smoke_tests/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "16:30"
BLOCK = "release"
TRIGGER = "webhook: deploy.succeeded(staging)"
AUTOMATION = "testing"

USECASE = UseCase(
    id=70,
    domain="swe-" + BLOCK,
    title="Smoke tests on staging",
    ask="Run smoke tests against staging.",
    why="Runs the suites in parallel and reports only what matters.",
    tools=[TOOL("smoke", "Run a smoke suite.", lambda suite: {"suite": suite, "passed": True}, {"suite": str})],
    plan=[par(call("smoke", suite="payments"), call("smoke", suite="refunds"), call("smoke", suite="webhooks")),
          say("All 3 smoke suites pass on staging.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
