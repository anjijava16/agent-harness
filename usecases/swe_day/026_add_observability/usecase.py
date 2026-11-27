"""Add logging and metrics to an endpoint

When:     10:45 (coding)
Trigger:  manual
Type:     instrumentation

Mechanical but easy to get wrong; the team's conventions are in AGENTS.md.

Run:  python usecases/swe_day/026_add_observability/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/026_add_observability/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "10:45"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "instrumentation"

USECASE = UseCase(
    id=26,
    domain="swe-" + BLOCK,
    title="Add logging and metrics to an endpoint",
    ask="Add structured logging and a latency metric to create_payment.",
    why="Mechanical but easy to get wrong; the team's conventions are in AGENTS.md.",
    tools=[],
    agents_md="# Observability rules\n- Use log.info with event= and ids, never raw payloads\n- Metric names: service_action_seconds\n",
    seed_files={"/repo/payments/api.py": "def create_payment(req):\n    return store.save(req)\n"},
    plan=[read("/repo/payments/api.py"),
          edit("/repo/payments/api.py", "def create_payment(req):\n    return store.save(req)",
               "def create_payment(req):\n    with metrics.timer('payments_create_seconds'):\n        log.info('payment.create', event='create', id=req.id)\n        return store.save(req)"),
          say("create_payment now logs event=create with the id only and records payments_create_seconds.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
