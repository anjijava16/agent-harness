"""Meeting prep pack

When:     07:10 (morning)
Trigger:  cron: 10 7 * * 1-5
Type:     scheduled prep

Fetches the docs and open questions for each meeting so you walk in with context.

Run:  python usecases/swe_day/005_meeting_prep_pack/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/005_meeting_prep_pack/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "07:10"
BLOCK = "morning"
TRIGGER = "cron: 10 7 * * 1-5"
AUTOMATION = "scheduled prep"

USECASE = UseCase(
    id=5,
    domain="swe-" + BLOCK,
    title="Meeting prep pack",
    ask="Prep me for today's meetings.",
    why="Fetches the docs and open questions for each meeting so you walk in with context.",
    tools=[TOOL("calendar_today", "Today's meetings.", [{"t": "10:00", "title": "Ledger sharding design review", "doc": "DOC-77"},
                                                       {"t": "15:00", "title": "Sprint planning", "doc": "JIRA board"}]),
           TOOL("get_doc", "Fetch a doc's open comments.", lambda id: {"DOC-77": "3 open comments: hot partitions, backfill time, rollback"}.get(id, "n/a"),
                {"id": str})],
    plan=[call("calendar_today", query="today"), call("get_doc", id="DOC-77"),
          write("/prep/today.md", "10:00 Ledger sharding review: open questions = hot partitions, backfill time, rollback.\n15:00 Sprint planning.\n"),
          say("Two meetings. For the 10:00 sharding review, the open questions are hot partitions, backfill time and rollback. Prep saved.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
