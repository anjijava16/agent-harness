"""Kubernetes CrashLoopBackOff debug

When:     14:15 (ops)
Trigger:  webhook: pod_crashloop
Type:     troubleshooting

Reads pod events and previous logs, finds the cause, suggests the fix.

Run:  python usecases/swe_day/054_k8s_crashloop_debug/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/054_k8s_crashloop_debug/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "14:15"
BLOCK = "ops"
TRIGGER = "webhook: pod_crashloop"
AUTOMATION = "troubleshooting"

USECASE = UseCase(
    id=54,
    domain="swe-" + BLOCK,
    title="Kubernetes CrashLoopBackOff debug",
    ask="ledger-worker is in CrashLoopBackOff.",
    why="Reads pod events and previous logs, finds the cause, suggests the fix.",
    tools=[TOOL("pod_events", "kubectl describe events.", ["Back-off restarting failed container", "OOMKilled"], {"pod": str}),
           TOOL("previous_logs", "kubectl logs --previous.", "loading 2.1GB snapshot into memory...", {"pod": str}),
           TOOL("pod_limits", "Resource limits.", {"memory": "1Gi"}, {"pod": str})],
    plan=[par(call("pod_events", pod="ledger-worker"), call("previous_logs", pod="ledger-worker"), call("pod_limits", pod="ledger-worker")),
          say("OOMKilled: it loads a 2.1 GB snapshot with a 1 Gi limit. Stream the snapshot, or raise the limit to 3Gi short term.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
