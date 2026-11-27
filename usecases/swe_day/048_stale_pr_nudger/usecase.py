"""Stale PR nudger

When:     13:25 (review)
Trigger:  cron: 25 13 * * 1-5
Type:     reminders

Runs after lunch so PRs don't rot. Messages go out after one approval.

Run:  python usecases/swe_day/048_stale_pr_nudger/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/048_stale_pr_nudger/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "13:25"
BLOCK = "review"
TRIGGER = "cron: 25 13 * * 1-5"
AUTOMATION = "reminders"

USECASE = UseCase(
    id=48,
    domain="swe-" + BLOCK,
    title="Stale PR nudger",
    ask="Nudge reviewers on PRs waiting more than 2 days.",
    why="Runs after lunch so PRs don't rot. Messages go out after one approval.",
    tools=[TOOL("open_prs", "Open PRs with wait time.", [{"pr": 801, "reviewer": "ana", "waiting_days": 3}, {"pr": 815, "reviewer": "kai", "waiting_days": 1}]),
           TOOL("slack_dm", "DM someone on Slack.", "sent", {"user": str, "text": str}, "external")],
    plan=[call("open_prs", query="team"),
          call("slack_dm", user="ana", text="Hey, #801 has been waiting 3 days for your review when you get a minute."),
          say("Nudged ana about #801. #815 is only a day old, left it.")],
    hitl={"slack_dm": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
