"""Sprint board health check

When:     08:00 (morning)
Trigger:  cron: 0 8 * * 1-5
Type:     scheduled check

Spots blocked and stale tickets early. Typed output feeds a team dashboard.

Run:  python usecases/swe_day/011_sprint_board_health/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/011_sprint_board_health/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "08:00"
BLOCK = "morning"
TRIGGER = "cron: 0 8 * * 1-5"
AUTOMATION = "scheduled check"

USECASE = UseCase(
    id=11,
    domain="swe-" + BLOCK,
    title="Sprint board health check",
    ask="Is the sprint on track?",
    why="Spots blocked and stale tickets early. Typed output feeds a team dashboard.",
    tools=[TOOL("sprint_tickets", "Tickets in the active sprint.",
                [{"key": "PAY-428", "status": "blocked", "days_in_status": 4}, {"key": "PAY-431", "status": "in_progress", "days_in_status": 2},
                 {"key": "PAY-433", "status": "todo", "days_in_status": 9}])],
    plan=[call("sprint_tickets", query="active"),
          answer("SprintHealth", blocked=["PAY-428"], stale=["PAY-433"], on_track=False, note="PAY-428 blocked 4 days on infra")],
    output=("SprintHealth", {"blocked": list, "stale": list, "on_track": bool, "note": str})
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
