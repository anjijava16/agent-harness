"""Design doc first draft

When:     09:20 (planning)
Trigger:  manual
Type:     doc drafting

Follows the team's design-doc skill so every doc has the same sections reviewers expect.

Run:  python usecases/swe_day/018_design_doc_first_draft/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/018_design_doc_first_draft/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "09:20"
BLOCK = "planning"
TRIGGER = "manual"
AUTOMATION = "doc drafting"

USECASE = UseCase(
    id=18,
    domain="swe-" + BLOCK,
    title="Design doc first draft",
    ask="Draft a design doc for idempotency keys.",
    why="Follows the team's design-doc skill so every doc has the same sections reviewers expect.",
    tools=[TOOL("get_ticket", "Fetch a ticket.", {"key": "PAY-431", "title": "Idempotency keys"}, {"key": str})],
    skills={"design-doc": ("Use when writing design docs.", ["Context", "Goals / non-goals", "Design", "Alternatives", "Rollout", "Risks"])},
    plan=[read("/skills/design-doc/SKILL.md"), call("get_ticket", key="PAY-431"),
          write("/docs/design/idempotency_keys.md", "## Context\n## Goals\n## Design\nStore key->response 24h\n## Alternatives\n## Rollout\n## Risks\n"),
          say("Design doc drafted with all six standard sections. Biggest open item: where to store keys (Postgres vs Redis).")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
