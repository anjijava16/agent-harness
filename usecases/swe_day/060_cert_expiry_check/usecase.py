"""TLS certificate expiry check

When:     15:15 (ops)
Trigger:  cron: 0 15 * * 1
Type:     monitoring

Weekly; boring until the week it saves an outage.

Run:  python usecases/swe_day/060_cert_expiry_check/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/060_cert_expiry_check/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "15:15"
BLOCK = "ops"
TRIGGER = "cron: 0 15 * * 1"
AUTOMATION = "monitoring"

USECASE = UseCase(
    id=60,
    domain="swe-" + BLOCK,
    title="TLS certificate expiry check",
    ask="Any certs expiring in the next 30 days?",
    why="Weekly; boring until the week it saves an outage.",
    tools=[TOOL("cert_inventory", "All certs and days to expiry.", [{"host": "api.pay.example.com", "days": 12}, {"host": "admin.pay.example.com", "days": 80}])],
    plan=[call("cert_inventory", query="all"),
          say("api.pay.example.com expires in 12 days. cert-manager should have renewed it, so check the ACME challenge.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
