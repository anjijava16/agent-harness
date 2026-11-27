"""Find who owns the code you're about to change

When:     09:55 (planning)
Trigger:  manual
Type:     lookup

Combines CODEOWNERS with recent git history so you tag the right people.

Run:  python usecases/swe_day/022_find_code_owners/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/022_find_code_owners/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "09:55"
BLOCK = "planning"
TRIGGER = "manual"
AUTOMATION = "lookup"

USECASE = UseCase(
    id=22,
    domain="swe-" + BLOCK,
    title="Find who owns the code you're about to change",
    ask="Who should review changes to payments/store.py?",
    why="Combines CODEOWNERS with recent git history so you tag the right people.",
    tools=[TOOL("git_log_authors", "Top recent authors of a file.", [{"author": "ana", "commits": 14}, {"author": "kai", "commits": 3}], {"path": str})],
    seed_files={"/repo/CODEOWNERS": "payments/ @payments-team\npayments/store.py @ana\n"},
    plan=[read("/repo/CODEOWNERS"), call("git_log_authors", path="payments/store.py"),
          say("Tag @ana: she's the CODEOWNER for payments/store.py and wrote 14 of its recent commits.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
