"""Acceptance criteria generator

When:     08:40 (planning)
Trigger:  manual
Type:     ticket refinement

Turns a vague ticket into testable Given/When/Then criteria in a fixed schema.

Run:  python usecases/swe_day/014_acceptance_criteria_generator/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/014_acceptance_criteria_generator/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "08:40"
BLOCK = "planning"
TRIGGER = "manual"
AUTOMATION = "ticket refinement"

USECASE = UseCase(
    id=14,
    domain="swe-" + BLOCK,
    title="Acceptance criteria generator",
    ask="Write acceptance criteria for 'export invoices as CSV'.",
    why="Turns a vague ticket into testable Given/When/Then criteria in a fixed schema.",
    tools=[TOOL("get_ticket", "Fetch a ticket.", {"key": "PAY-440", "title": "Export invoices as CSV", "desc": "users want CSV"}, {"key": str})],
    plan=[call("get_ticket", key="PAY-440"),
          answer("AcceptanceCriteria", criteria=["Given invoices exist, when I click Export, then a CSV downloads",
                                                 "CSV has id, customer, amount, status, due_date",
                                                 "Exports over 10k rows are emailed instead"], edge_cases=["zero invoices", "unicode names"])],
    output=("AcceptanceCriteria", {"criteria": list, "edge_cases": list})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
