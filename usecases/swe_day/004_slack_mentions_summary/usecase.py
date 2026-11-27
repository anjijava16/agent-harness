"""Slack mentions and DMs summary

When:     07:00 (morning)
Trigger:  cron: 0 7 * * 1-5
Type:     scheduled digest

Separates what needs a reply from FYIs. Read-only: it never answers for you.

Run:  python usecases/swe_day/004_slack_mentions_summary/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/004_slack_mentions_summary/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "07:00"
BLOCK = "morning"
TRIGGER = "cron: 0 7 * * 1-5"
AUTOMATION = "scheduled digest"

USECASE = UseCase(
    id=4,
    domain="swe-" + BLOCK,
    title="Slack mentions and DMs summary",
    ask="Summarize my Slack mentions and DMs since yesterday evening.",
    why="Separates what needs a reply from FYIs. Read-only: it never answers for you.",
    tools=[TOOL("slack_mentions", "Mentions and DMs since a time.",
                [{"from": "ana", "ch": "#payments", "text": "@sam can you look at P-302 disk alert?"},
                 {"from": "kai", "ch": "DM", "text": "FYI design review moved to 3pm"}], {"since": str})],
    plan=[call("slack_mentions", since="18:00 yesterday"),
          say("Needs you: Ana asked you to look at the P-302 disk alert (#payments). FYI: design review moved to 3pm (Kai).")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
