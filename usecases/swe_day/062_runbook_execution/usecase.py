"""Follow a runbook step by step

When:     15:35 (ops)
Trigger:  manual
Type:     runbook

Reads the runbook and runs it as a todo list; the cordon/drain steps need approval.

Run:  python usecases/swe_day/062_runbook_execution/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/062_runbook_execution/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "15:35"
BLOCK = "ops"
TRIGGER = "manual"
AUTOMATION = "runbook"

USECASE = UseCase(
    id=62,
    domain="swe-" + BLOCK,
    title="Follow a runbook step by step",
    ask="Run the 'drain a node' runbook for node ip-10-0-3-7.",
    why="Reads the runbook and runs it as a todo list; the cordon/drain steps need approval.",
    tools=[TOOL("kubectl", "Run a kubectl command.", "ok", {"cmd": str}, "write")],
    seed_files={"/runbooks/drain-node.md": "1. cordon\n2. drain --ignore-daemonsets\n3. verify pods rescheduled\n"},
    plan=[read("/runbooks/drain-node.md"), todos("cordon", "drain", "verify"),
          call("kubectl", cmd="cordon ip-10-0-3-7"), call("kubectl", cmd="drain ip-10-0-3-7 --ignore-daemonsets"),
          say("Node cordoned and drained; all pods rescheduled.")],
    hitl={"kubectl": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
