"""Reproduce a bug from a support ticket

When:     15:45 (ops)
Trigger:  webhook: zendesk_ticket_tagged_bug
Type:     bug repro

Writes a failing test that reproduces the report; the fix comes after.

Run:  python usecases/swe_day/064_support_ticket_reproduction/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/064_support_ticket_reproduction/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "15:45"
BLOCK = "ops"
TRIGGER = "webhook: zendesk_ticket_tagged_bug"
AUTOMATION = "bug repro"

USECASE = UseCase(
    id=64,
    domain="swe-" + BLOCK,
    title="Reproduce a bug from a support ticket",
    ask="Support says invoices with emoji in the name fail to export. Reproduce it.",
    why="Writes a failing test that reproduces the report; the fix comes after.",
    tools=[TOOL("get_support_ticket", "Support ticket.", {"id": 5512, "text": "Customer 'Café ☕' export fails with 500"}, {"id": int}),
           TOOL("run_tests", "Run tests.", {"passed": 0, "failed": 1, "error": "UnicodeEncodeError: 'latin-1'"}, {"path": str})],
    plan=[call("get_support_ticket", id=5512),
          write("/repo/tests/test_export_unicode.py", "def test_emoji_customer_export():\n    assert export_csv([{'customer': 'Café ☕'}])\n"),
          call("run_tests", path="tests/test_export_unicode.py"),
          say("Reproduced: UnicodeEncodeError, the CSV writer uses latin-1. Failing test added; fix is encoding='utf-8'.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
