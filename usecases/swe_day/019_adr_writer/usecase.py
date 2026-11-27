"""Architecture decision record

When:     09:30 (planning)
Trigger:  manual
Type:     doc drafting

Captures a decision in the repo's ADR format while the reasoning is fresh.

Run:  python usecases/swe_day/019_adr_writer/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/019_adr_writer/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "09:30"
BLOCK = "planning"
TRIGGER = "manual"
AUTOMATION = "doc drafting"

USECASE = UseCase(
    id=19,
    domain="swe-" + BLOCK,
    title="Architecture decision record",
    ask="Write an ADR for choosing Arq for background jobs.",
    why="Captures a decision in the repo's ADR format while the reasoning is fresh.",
    tools=[TOOL("next_adr_number", "Next ADR number in the repo.", 17)],
    seed_files={"/repo/docs/adr/0016-postgres-for-ledger.md": "# 16. Postgres for ledger\nStatus: accepted\n"},
    plan=[ls("/repo/docs/adr"), call("next_adr_number", query="repo"),
          write("/repo/docs/adr/0017-arq-for-background-jobs.md", "# 17. Arq for background jobs\nStatus: proposed\n## Context\n## Decision\n## Consequences\n"),
          say("ADR 0017 written (status: proposed).")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
