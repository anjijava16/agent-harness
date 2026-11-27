"""First-pass PR review

When:     12:30 (review)
Trigger:  webhook: pull_request.opened
Type:     code review

A reviewer subagent reads the diff in its own context; posting the review is a write you
approve.

Run:  python usecases/swe_day/039_pr_review_with_reviewer_subagent/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/039_pr_review_with_reviewer_subagent/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "12:30"
BLOCK = "review"
TRIGGER = "webhook: pull_request.opened"
AUTOMATION = "code review"

USECASE = UseCase(
    id=39,
    domain="swe-" + BLOCK,
    title="First-pass PR review",
    ask="Review PR #812 and leave comments.",
    why="A reviewer subagent reads the diff in its own context; posting the review is a write you approve.",
    tools=[TOOL("get_diff", "Get a PR diff.", "+ def refund(amount):\n+     return amount * -1\n+ # TODO handle currency", {"pr": int}),
           TOOL("post_review", "Post review comments to a PR.", "posted", {"pr": int, "body": str}, "external")],
    subagents=[SUB("reviewer", "Reviews diffs for bugs and style.", ["get_diff"],
                   [call("get_diff", pr=812), say("1) refund() ignores currency (TODO left in). 2) No test for negative amounts.")])],
    plan=[task("reviewer", "Review PR #812"),
          call("post_review", pr=812, body="1) refund() ignores currency. 2) Please add a test for negative amounts."),
          say("Posted 2 comments on #812: currency is ignored, and negative amounts aren't tested.")],
    hitl={"post_review": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
