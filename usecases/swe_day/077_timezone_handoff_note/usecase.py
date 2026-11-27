"""Handoff note for the other timezone

When:     17:50 (release)
Trigger:  cron: 50 17 * * 1-5
Type:     handoff

So the morning team in another timezone doesn't start by asking what happened.

Run:  python usecases/swe_day/077_timezone_handoff_note/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/077_timezone_handoff_note/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "17:50"
BLOCK = "release"
TRIGGER = "cron: 50 17 * * 1-5"
AUTOMATION = "handoff"

USECASE = UseCase(
    id=77,
    domain="swe-" + BLOCK,
    title="Handoff note for the other timezone",
    ask="Write the handoff for the Bangalore team.",
    why="So the morning team in another timezone doesn't start by asking what happened.",
    tools=[TOOL("open_incidents", "Open incidents.", [{"id": "INC-77", "status": "monitoring"}]),
           TOOL("in_flight_deploys", "Deploys in progress.", [{"service": "payments-api", "version": "v2.32.0", "canary": "10%"}])],
    plan=[par(call("open_incidents", query="payments"), call("in_flight_deploys", query="payments")),
          write("/handoff/today.md", "- INC-77 monitoring, no action\n- v2.32.0 at 10% canary: promote to 50% if metrics flat at your 10:00\n"),
          say("Handoff written: INC-77 is monitoring, and v2.32.0 can go to 50% in their morning if metrics stay flat.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
