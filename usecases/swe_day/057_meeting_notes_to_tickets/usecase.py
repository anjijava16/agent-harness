"""Meeting notes to tickets

When:     14:45 (ops)
Trigger:  webhook: meeting_transcript_ready
Type:     ticket creation

Pulls the action items out and creates tickets; one isn't a real task and gets rejected.

Run:  python usecases/swe_day/057_meeting_notes_to_tickets/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/057_meeting_notes_to_tickets/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "14:45"
BLOCK = "ops"
TRIGGER = "webhook: meeting_transcript_ready"
AUTOMATION = "ticket creation"

USECASE = UseCase(
    id=57,
    domain="swe-" + BLOCK,
    title="Meeting notes to tickets",
    ask="Turn the architecture sync transcript into tickets.",
    why="Pulls the action items out and creates tickets; one isn't a real task and gets rejected.",
    tools=[TOOL("get_transcript", "Meeting transcript.", "Ana: we need a retry dashboard. Kai: I'll look at Redis memory. Me: someone should buy pizza.", {"meeting": str}),
           TOOL("create_ticket", "Create a ticket.", "created", {"title": str, "owner": str}, "write")],
    plan=[call("get_transcript", meeting="arch-sync"),
          par(call("create_ticket", title="Webhook retry dashboard", owner="ana"), call("create_ticket", title="Investigate Redis memory", owner="kai"),
              call("create_ticket", title="Buy pizza", owner="me")),
          say("Created 2 tickets (retry dashboard, Redis memory). Skipped the pizza one.")],
    hitl={"create_ticket": ["approve", "approve", "reject"]},
    expect=[("no pizza ticket", lambda c: all("pizza" not in a["args"]["title"].lower() for a in c["world"].actions))]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
