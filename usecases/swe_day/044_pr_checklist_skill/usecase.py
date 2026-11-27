"""PR checklist check

When:     13:05 (review)
Trigger:  webhook: pull_request.opened
Type:     policy check

The checklist lives in a skill, so changing the rules means editing one file.

Run:  python usecases/swe_day/044_pr_checklist_skill/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/044_pr_checklist_skill/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "13:05"
BLOCK = "review"
TRIGGER = "webhook: pull_request.opened"
AUTOMATION = "policy check"

USECASE = UseCase(
    id=44,
    domain="swe-" + BLOCK,
    title="PR checklist check",
    ask="Does PR #820 meet our merge checklist?",
    why="The checklist lives in a skill, so changing the rules means editing one file.",
    tools=[TOOL("pr_facts", "Facts about a PR.", {"tests_changed": True, "migration": True, "down_migration": False, "docs_changed": False}, {"pr": int})],
    skills={"pr-checklist": ("Use for merge readiness.", ["Tests changed", "Migrations have down scripts", "Docs updated for API changes"])},
    plan=[read("/skills/pr-checklist/SKILL.md"), call("pr_facts", pr=820),
          answer("Checklist", passed=["tests changed"], failed=["migration has no down script", "docs not updated"])],
    output=("Checklist", {"passed": list, "failed": list})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
