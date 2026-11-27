"""Scale a deployment

When:     13:50 (ops)
Trigger:  webhook: hpa_maxed
Type:     capacity

Scaling within the limit is allowed; going past the cost cap is blocked.

Run:  python usecases/swe_day/051_scale_deployment/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/051_scale_deployment/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "13:50"
BLOCK = "ops"
TRIGGER = "webhook: hpa_maxed"
AUTOMATION = "capacity"

USECASE = UseCase(
    id=51,
    domain="swe-" + BLOCK,
    title="Scale a deployment",
    ask="payments-api is CPU bound. Scale it up.",
    why="Scaling within the limit is allowed; going past the cost cap is blocked.",
    tools=[TOOL("scale", "Set replica count.", "scaled", {"deployment": str, "replicas": int}, "write"),
           TOOL("cpu_usage", "CPU utilisation.", {"avg": 0.92, "replicas": 6}, {"deployment": str})],
    plan=[call("cpu_usage", deployment="payments-api"),
          call("scale", deployment="payments-api", replicas=40),
          call("scale", deployment="payments-api", replicas=10),
          say("Scaled payments-api from 6 to 10 replicas. 40 was over the 20-replica cap.")],
    guard={"scale": lambda a: "over 20-replica cap" if a["replicas"] > 20 else None},
    expect=[("scaled to 10", lambda c: c["world"].actions[-1]["args"]["replicas"] == 10)]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
