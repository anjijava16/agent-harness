"""Unused feature flag report

When:     23:45 (night)
Trigger:  cron: 45 23 1 * *
Type:     cleanup

Flags pile up. This finds the dead ones and where they live in code.

Run:  python usecases/swe_day/096_unused_feature_flags/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/096_unused_feature_flags/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "23:45"
BLOCK = "night"
TRIGGER = "cron: 45 23 1 * *"
AUTOMATION = "cleanup"

USECASE = UseCase(
    id=96,
    domain="swe-" + BLOCK,
    title="Unused feature flag report",
    ask="Which feature flags are 100% on everywhere and can be removed from code?",
    why="Flags pile up. This finds the dead ones and where they live in code.",
    tools=[TOOL("flag_states", "All flags and rollout per env.", [{"flag": "new_checkout", "prod": 100, "days_unchanged": 120}, {"flag": "invoice_export", "prod": 0}]),
           TOOL("search_code", "Search code.", ["checkout/flow.py:22 if flags.on('new_checkout'):"], {"query": str})],
    plan=[call("flag_states", query="all"), call("search_code", query="new_checkout"),
          say("new_checkout has been 100% on for 120 days. Remove it from checkout/flow.py:22.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
