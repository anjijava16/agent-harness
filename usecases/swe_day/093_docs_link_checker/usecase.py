"""Broken docs link checker

When:     23:20 (night)
Trigger:  cron: 20 23 * * 0
Type:     docs

Fixes the ones with an obvious redirect, lists the rest.

Run:  python usecases/swe_day/093_docs_link_checker/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/093_docs_link_checker/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "23:20"
BLOCK = "night"
TRIGGER = "cron: 20 23 * * 0"
AUTOMATION = "docs"

USECASE = UseCase(
    id=93,
    domain="swe-" + BLOCK,
    title="Broken docs link checker",
    ask="Find and fix broken links in docs/.",
    why="Fixes the ones with an obvious redirect, lists the rest.",
    tools=[TOOL("check_links", "Check links in docs.", [{"file": "/repo/docs/api/payments.md", "url": "/docs/v1/errors", "status": 404, "redirect": "/docs/errors"}])],
    seed_files={"/repo/docs/api/payments.md": "See [errors](/docs/v1/errors).\n"},
    plan=[call("check_links", query="docs"),
          edit("/repo/docs/api/payments.md", "(/docs/v1/errors)", "(/docs/errors)"),
          say("Fixed 1 broken link (/docs/v1/errors to /docs/errors).")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
