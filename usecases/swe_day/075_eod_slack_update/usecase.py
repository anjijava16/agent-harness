"""End-of-day Slack update

When:     17:30 (release)
Trigger:  cron: 30 17 * * 1-5
Type:     status update

Built from what actually happened today. You edit the message before it posts.

Run:  python usecases/swe_day/075_eod_slack_update/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/075_eod_slack_update/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "17:30"
BLOCK = "release"
TRIGGER = "cron: 30 17 * * 1-5"
AUTOMATION = "status update"

USECASE = UseCase(
    id=75,
    domain="swe-" + BLOCK,
    title="End-of-day Slack update",
    ask="Post my end-of-day update to #payments-team.",
    why="Built from what actually happened today. You edit the message before it posts.",
    tools=[TOOL("my_activity_today", "PRs, deploys, tickets you touched today.", {"merged": [820], "reviewed": [812], "deployed": ["v2.32.0"]}),
           TOOL("slack_post", "Post to a Slack channel.", "posted", {"channel": str, "text": str}, "external")],
    plan=[call("my_activity_today", query="me"),
          call("slack_post", channel="#payments-team", text="Merged #820, reviewed #812, shipped v2.32.0."),
          say("EOD update posted.")],
    hitl={"slack_post": ("edit", {"text": "Merged #820 (idempotency keys), reviewed #812, shipped v2.32.0 to 10% canary. Tomorrow: finish CSV export."})}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
