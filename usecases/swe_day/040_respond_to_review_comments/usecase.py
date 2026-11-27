"""Address review comments on your PR

When:     12:40 (review)
Trigger:  webhook: pull_request_review.submitted
Type:     code review

Reads each comment, makes the code change, drafts the replies.

Run:  python usecases/swe_day/040_respond_to_review_comments/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/040_respond_to_review_comments/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "12:40"
BLOCK = "review"
TRIGGER = "webhook: pull_request_review.submitted"
AUTOMATION = "code review"

USECASE = UseCase(
    id=40,
    domain="swe-" + BLOCK,
    title="Address review comments on your PR",
    ask="Address the review comments on my PR #805.",
    why="Reads each comment, makes the code change, drafts the replies.",
    tools=[TOOL("get_review_comments", "Review comments on a PR.",
                [{"id": 1, "file": "payments/api.py", "body": "rename x to amount"}, {"id": 2, "file": "payments/api.py", "body": "why not use Decimal?"}], {"pr": int}),
           TOOL("reply_comment", "Reply to a review comment.", "replied", {"id": int, "body": str}, "external")],
    seed_files={"/repo/payments/api.py": "def charge(x):\n    return float(x)\n"},
    plan=[call("get_review_comments", pr=805),
          edit("/repo/payments/api.py", "def charge(x):\n    return float(x)", "from decimal import Decimal\n\ndef charge(amount):\n    return Decimal(amount)"),
          par(call("reply_comment", id=1, body="Renamed."), call("reply_comment", id=2, body="Good call, switched to Decimal.")),
          say("Both comments addressed in code and replied to.")],
    hitl={"reply_comment": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
