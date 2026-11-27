"""PR review queue prioritizer

When:     06:50 (morning)
Trigger:  cron: 50 6 * * 1-5
Type:     scheduled triage

Ranks review requests by blocking impact and age; output is typed so a Slack bot can post
it.

Run:  python usecases/swe_day/003_pr_review_queue_prioritizer/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/003_pr_review_queue_prioritizer/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "06:50"
BLOCK = "morning"
TRIGGER = "cron: 50 6 * * 1-5"
AUTOMATION = "scheduled triage"

USECASE = UseCase(
    id=3,
    domain="swe-" + BLOCK,
    title="PR review queue prioritizer",
    ask="Which PRs should I review first today?",
    why="Ranks review requests by blocking impact and age; output is typed so a Slack bot can post it.",
    tools=[TOOL("review_requests", "PRs where I'm a requested reviewer.",
                [{"pr": 812, "age_h": 30, "blocks_release": True, "lines": 120}, {"pr": 815, "age_h": 4, "blocks_release": False, "lines": 900},
                 {"pr": 809, "age_h": 52, "blocks_release": False, "lines": 40}])],
    plan=[call("review_requests", query="me"),
          answer("ReviewQueue", order=[812, 809, 815], reason="812 blocks release; 809 is small and 2 days old; 815 is big, book time")],
    output=("ReviewQueue", {"order": list, "reason": str}),
    expect=[("release blocker first", lambda c: c["structured"].order[0] == 812)]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
