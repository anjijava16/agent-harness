"""Dependabot PR batch triage

When:     07:30 (morning)
Trigger:  cron: 30 7 * * 1-5
Type:     auto-merge with approval

Patch bumps with green CI get merged after one approval for the batch; majors are left for
a human.

Run:  python usecases/swe_day/007_dependabot_batch_triage/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/007_dependabot_batch_triage/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "07:30"
BLOCK = "morning"
TRIGGER = "cron: 30 7 * * 1-5"
AUTOMATION = "auto-merge with approval"

USECASE = UseCase(
    id=7,
    domain="swe-" + BLOCK,
    title="Dependabot PR batch triage",
    ask="Handle this morning's dependency bump PRs.",
    why="Patch bumps with green CI get merged after one approval for the batch; majors are left for a human.",
    tools=[TOOL("dependency_prs", "Open dependency PRs.", [{"pr": 901, "pkg": "pydantic", "bump": "patch", "ci": "green"},
                                                          {"pr": 902, "pkg": "sqlalchemy", "bump": "major", "ci": "green"},
                                                          {"pr": 903, "pkg": "httpx", "bump": "patch", "ci": "green"}]),
           TOOL("merge_pr", "Merge a PR.", "merged", {"pr": int}, "write")],
    plan=[call("dependency_prs", query="open"),
          par(call("merge_pr", pr=901), call("merge_pr", pr=903), call("merge_pr", pr=902)),
          say("Merged the 2 patch bumps (pydantic, httpx). sqlalchemy 2.x is a major bump and needs a human review.")],
    hitl={"merge_pr": "approve"},
    guard={"merge_pr": lambda a: "major version bumps need manual review" if a["pr"] == 902 else None},
    expect=[("only patch bumps merged", lambda c: sorted(x["args"]["pr"] for x in c["world"].actions) == [901, 903])]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
