"""Roll back a bad deploy

When:     13:40 (ops)
Trigger:  manual: from incident
Type:     deploy

A rollback touches prod, so it waits for your approval.

Run:  python usecases/swe_day/050_rollback_deploy/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/050_rollback_deploy/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "13:40"
BLOCK = "ops"
TRIGGER = "manual: from incident"
AUTOMATION = "deploy"

USECASE = UseCase(
    id=50,
    domain="swe-" + BLOCK,
    title="Roll back a bad deploy",
    ask="Roll checkout back to v2.30.4.",
    why="A rollback touches prod, so it waits for your approval.",
    tools=[TOOL("rollback", "Roll a service back to a version.", "rolled back", {"service": str, "version": str}, "write"),
           TOOL("error_rate", "5xx rate.", {"now": 0.002}, {"service": str})],
    plan=[call("rollback", service="checkout", version="v2.30.4"), call("error_rate", service="checkout"),
          say("checkout is on v2.30.4 and 5xx is back to 0.2%.")],
    hitl={"rollback": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
