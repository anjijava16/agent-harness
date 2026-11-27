"""Nightly secrets scan across repos

When:     23:40 (night)
Trigger:  cron: 40 23 * * *
Type:     security

Opening a security ticket is allowed; the raw secret value never leaves the scan tool.

Run:  python usecases/swe_day/095_secrets_scan_repos/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/095_secrets_scan_repos/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "23:40"
BLOCK = "night"
TRIGGER = "cron: 40 23 * * *"
AUTOMATION = "security"

USECASE = UseCase(
    id=95,
    domain="swe-" + BLOCK,
    title="Nightly secrets scan across repos",
    ask="Scan all team repos for committed secrets.",
    why="Opening a security ticket is allowed; the raw secret value never leaves the scan tool.",
    tools=[TOOL("scan_secrets", "Scan a repo for secrets.", lambda repo: {"payments-api": [{"file": "scripts/dev.sh", "type": "aws_key", "fingerprint": "AKIA...7Q"}], "ledger": []}[repo], {"repo": str}),
           TOOL("create_ticket", "Create a ticket.", "created", {"title": str, "owner": str}, "write")],
    plan=[par(call("scan_secrets", repo="payments-api"), call("scan_secrets", repo="ledger")),
          call("create_ticket", title="Rotate AWS key in payments-api scripts/dev.sh (AKIA...7Q)", owner="security"),
          say("Found one AWS key in payments-api/scripts/dev.sh and opened a ticket for security. ledger is clean.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
