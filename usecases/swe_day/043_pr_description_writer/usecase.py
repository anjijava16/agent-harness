"""Write the PR description

When:     13:00 (review)
Trigger:  manual
Type:     docs

Builds the description from commits and the diff, in the repo's PR template.

Run:  python usecases/swe_day/043_pr_description_writer/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/043_pr_description_writer/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "13:00"
BLOCK = "review"
TRIGGER = "manual"
AUTOMATION = "docs"

USECASE = UseCase(
    id=43,
    domain="swe-" + BLOCK,
    title="Write the PR description",
    ask="Write a PR description for my branch.",
    why="Builds the description from commits and the diff, in the repo's PR template.",
    tools=[TOOL("branch_commits", "Commits on the current branch.", ["add idempotency table", "middleware", "tests"]),
           TOOL("update_pr", "Update a PR body.", "updated", {"pr": int, "body": str}, "external")],
    seed_files={"/repo/.github/pull_request_template.md": "## What\n## Why\n## How tested\n"},
    plan=[par(call("branch_commits", query="HEAD"), read("/repo/.github/pull_request_template.md")),
          call("update_pr", pr=820, body="## What\nIdempotency keys\n## Why\nPAY-431\n## How tested\nunit + integration\n"),
          say("PR #820 description filled in from the template and 3 commits.")],
    hitl={"update_pr": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
