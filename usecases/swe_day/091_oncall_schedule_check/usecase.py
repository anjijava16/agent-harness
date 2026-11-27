"""On-call schedule gap check

When:     23:00 (night)
Trigger:  cron: 0 23 * * 4
Type:     scheduling

Cross-checks the rota against PTO so nobody finds the gap at 3am.

Run:  python usecases/swe_day/091_oncall_schedule_check/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/091_oncall_schedule_check/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "23:00"
BLOCK = "night"
TRIGGER = "cron: 0 23 * * 4"
AUTOMATION = "scheduling"

USECASE = UseCase(
    id=91,
    domain="swe-" + BLOCK,
    title="On-call schedule gap check",
    ask="Any gaps or conflicts in next week's on-call?",
    why="Cross-checks the rota against PTO so nobody finds the gap at 3am.",
    tools=[TOOL("oncall_rota", "Next week's rota.", [{"day": "Mon", "who": "kai"}, {"day": "Tue", "who": "ana"}, {"day": "Wed", "who": None}]),
           TOOL("pto", "PTO next week.", [{"who": "ana", "day": "Tue"}])],
    plan=[par(call("oncall_rota", query="next week"), call("pto", query="next week")),
          say("Two problems next week: Wednesday has nobody, and ana is on PTO Tuesday while on call.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
