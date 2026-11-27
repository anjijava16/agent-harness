"""Jira ticket to implementation plan

When:     08:30 (planning)
Trigger:  manual: ticket assigned
Type:     planning

Reads the ticket and the code it touches, then lays out the steps as a todo list you can
follow.

Run:  python usecases/swe_day/013_ticket_to_implementation_plan/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/013_ticket_to_implementation_plan/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "08:30"
BLOCK = "planning"
TRIGGER = "manual: ticket assigned"
AUTOMATION = "planning"

USECASE = UseCase(
    id=13,
    domain="swe-" + BLOCK,
    title="Jira ticket to implementation plan",
    ask="Turn PAY-431 into an implementation plan.",
    why="Reads the ticket and the code it touches, then lays out the steps as a todo list you can follow.",
    tools=[TOOL("get_ticket", "Fetch a Jira ticket.", {"key": "PAY-431", "title": "Idempotency keys for POST /payments",
                                                       "ac": ["same key returns same response", "keys expire after 24h"]}, {"key": str}),
           TOOL("search_code", "Search the codebase.", ["payments/api.py:create_payment", "payments/store.py"], {"query": str})],
    plan=[par(call("get_ticket", key="PAY-431"), call("search_code", query="def create_payment")),
          todos("Add idempotency_keys table", "Middleware: read Idempotency-Key header", "Store + replay response", "24h TTL job", "Tests"),
          write("/plans/PAY-431.md", "Touches payments/api.py and payments/store.py. New table idempotency_keys(key, response, expires_at).\n"),
          say("Plan for PAY-431: 5 steps, starting with an idempotency_keys table. Touches api.py and store.py. Saved to /plans/PAY-431.md.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
