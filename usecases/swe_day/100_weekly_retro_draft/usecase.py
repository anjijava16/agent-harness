"""Weekly retro draft

When:     23:59 (night)
Trigger:  cron: 59 23 * * 5
Type:     reflection

Reads the week's learnings from long-term memory and the shipped work, and drafts the
retro for Monday.

Run:  python usecases/swe_day/100_weekly_retro_draft/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/100_weekly_retro_draft/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "23:59"
BLOCK = "night"
TRIGGER = "cron: 59 23 * * 5"
AUTOMATION = "reflection"

USECASE = UseCase(
    id=100,
    domain="swe-" + BLOCK,
    title="Weekly retro draft",
    ask="Draft my weekly retro.",
    why="Reads the week's learnings from long-term memory and the shipped work, and drafts the retro for Monday.",
    tools=[TOOL("shipped_this_week", "Work shipped this week.", ["v2.32.0 idempotency + refunds", "INC-77 resolved"])],
    long_term_memory=True,
    plan=[write("/memories/learnings.md", "- KeyError currency = missing currency map\n"),
          read("/memories/learnings.md"), call("shipped_this_week", query="me"),
          write("/retro/week-48.md", "## Went well\n- Shipped idempotency keys\n## Didn't\n- INC-77 cost the checkout SLO\n## Try\n- Config validation in CI\n"),
          say("Retro drafted: shipped idempotency keys; INC-77 cost the checkout SLO; try config validation in CI next week.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
