"""Nightly dependency update PRs

When:     19:00 (night)
Trigger:  cron: 0 19 * * 1-5
Type:     maintenance

Runs unattended. Opening a PR is allowed; merging isn't a tool it has.

Run:  python usecases/swe_day/081_nightly_dependency_update_prs/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/081_nightly_dependency_update_prs/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "19:00"
BLOCK = "night"
TRIGGER = "cron: 0 19 * * 1-5"
AUTOMATION = "maintenance"

USECASE = UseCase(
    id=81,
    domain="swe-" + BLOCK,
    title="Nightly dependency update PRs",
    ask="Open PRs for safe dependency updates.",
    why="Runs unattended. Opening a PR is allowed; merging isn't a tool it has.",
    tools=[TOOL("outdated", "Outdated packages.", [{"pkg": "httpx", "from": "0.27.0", "to": "0.27.2"}, {"pkg": "pydantic", "from": "2.8", "to": "2.9"}]),
           TOOL("open_pr", "Open a PR.", "opened", {"title": str, "branch": str}, "external")],
    plan=[call("outdated", query="payments-api"),
          par(call("open_pr", title="Bump httpx to 0.27.2", branch="deps/httpx"), call("open_pr", title="Bump pydantic to 2.9", branch="deps/pydantic")),
          say("Opened 2 dependency PRs (httpx, pydantic). CI will tell us in the morning.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
