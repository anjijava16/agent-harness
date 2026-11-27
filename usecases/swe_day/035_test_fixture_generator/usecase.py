"""Generate realistic test fixtures

When:     12:15 (coding)
Trigger:  manual
Type:     test data

Reads the model definition so fixtures match the schema.

Run:  python usecases/swe_day/035_test_fixture_generator/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/035_test_fixture_generator/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "12:15"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "test data"

USECASE = UseCase(
    id=35,
    domain="swe-" + BLOCK,
    title="Generate realistic test fixtures",
    ask="Generate 5 invoice fixtures covering paid, overdue and disputed.",
    why="Reads the model definition so fixtures match the schema.",
    tools=[],
    seed_files={"/repo/payments/models.py": "class Invoice:\n    id: str\n    amount: float\n    status: str  # paid|open|overdue|disputed\n"},
    plan=[read("/repo/payments/models.py"),
          write("/repo/tests/fixtures/invoices.json",
                '[{"id":"INV-1","amount":100,"status":"paid"},{"id":"INV-2","amount":250,"status":"overdue"},{"id":"INV-3","amount":80,"status":"disputed"}]'),
          say("Fixtures written covering paid, overdue and disputed, matching the Invoice model.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
