"""Overnight incident recap

When:     06:40 (morning)
Trigger:  cron: 40 6 * * 1-5
Type:     scheduled digest

Pulls incidents and their timelines in parallel so you know the state of prod before
standup.

Run:  python usecases/swe_day/002_pagerduty_overnight_recap/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/002_pagerduty_overnight_recap/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "06:40"
BLOCK = "morning"
TRIGGER = "cron: 40 6 * * 1-5"
AUTOMATION = "scheduled digest"

USECASE = UseCase(
    id=2,
    domain="swe-" + BLOCK,
    title="Overnight incident recap",
    ask="What paged overnight and is anything still open?",
    why="Pulls incidents and their timelines in parallel so you know the state of prod before standup.",
    tools=[TOOL("list_incidents", "Incidents in a window.", [{"id": "P-301", "service": "payments-api", "status": "resolved", "dur_min": 18},
                                                            {"id": "P-302", "service": "ledger", "status": "acknowledged", "dur_min": 95}], {"since": str}),
           TOOL("incident_notes", "Timeline notes for an incident.", lambda id: {"P-301": "auto-resolved after pod restart",
                                                                                "P-302": "disk 92% on ledger-db-1, still growing"}[id], {"id": str})],
    plan=[call("list_incidents", since="22:00 yesterday"),
          par(call("incident_notes", id="P-301"), call("incident_notes", id="P-302")),
          say("P-301 payments-api resolved itself (18 min, pod restart). P-302 ledger is still open: ledger-db-1 disk at 92% and growing.")],
    expect=[("open incident flagged", lambda c: "P-302" in c["final"])]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
