"""Rotate a leaked secret

When:     14:55 (ops)
Trigger:  webhook: secret_scanning_alert
Type:     security

Rotation and redeploys touch prod and each needs approval. The agent follows the runbook
order.

Run:  python usecases/swe_day/058_rotate_leaked_secret/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/058_rotate_leaked_secret/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "14:55"
BLOCK = "ops"
TRIGGER = "webhook: secret_scanning_alert"
AUTOMATION = "security"

USECASE = UseCase(
    id=58,
    domain="swe-" + BLOCK,
    title="Rotate a leaked secret",
    ask="GitHub flagged a leaked Stripe key. Rotate it.",
    why="Rotation and redeploys touch prod and each needs approval. The agent follows the runbook order.",
    tools=[TOOL("rotate_key", "Rotate an API key at the provider.", "new key issued", {"key_id": str}, "write"),
           TOOL("update_secret", "Update the secret in the secret manager.", "updated", {"name": str}, "write"),
           TOOL("restart", "Rolling restart of a deployment.", "restarted", {"deployment": str}, "write")],
    plan=[todos("Rotate key at Stripe", "Update secret manager", "Restart consumers", "Confirm old key revoked"),
          call("rotate_key", key_id="sk_live_51H..."), call("update_secret", name="stripe/api_key"), call("restart", deployment="payments-api"),
          say("Key rotated, secret updated, payments-api restarted. Old key is revoked.")],
    hitl={"rotate_key": "approve", "update_secret": "approve", "restart": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
