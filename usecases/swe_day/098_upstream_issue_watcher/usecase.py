"""Watch upstream OSS issues we depend on

When:     23:55 (night)
Trigger:  cron: 55 23 * * *
Type:     monitoring

Checks issues you starred so you hear when a fix lands.

Run:  python usecases/swe_day/098_upstream_issue_watcher/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/098_upstream_issue_watcher/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "23:55"
BLOCK = "night"
TRIGGER = "cron: 55 23 * * *"
AUTOMATION = "monitoring"

USECASE = UseCase(
    id=98,
    domain="swe-" + BLOCK,
    title="Watch upstream OSS issues we depend on",
    ask="Any news on the upstream issues we're tracking?",
    why="Checks issues you starred so you hear when a fix lands.",
    tools=[TOOL("issue_status", "Status of a GitHub issue.", lambda repo, number: {"state": "closed", "fixed_in": "0.28.0"} if number == 3301 else {"state": "open"}, {"repo": str, "number": int})],
    plan=[par(call("issue_status", repo="encode/httpx", number=3301), call("issue_status", repo="pydantic/pydantic", number=9876)),
          say("httpx#3301 is fixed in 0.28.0, so we can drop our workaround. pydantic#9876 is still open.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
