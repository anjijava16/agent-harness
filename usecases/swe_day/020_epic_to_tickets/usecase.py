"""Break an epic into tickets

When:     09:40 (planning)
Trigger:  manual
Type:     ticket creation

Creating tickets is a write; the batch is approved, and one ticket is edited before
creation.

Run:  python usecases/swe_day/020_epic_to_tickets/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/020_epic_to_tickets/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "09:40"
BLOCK = "planning"
TRIGGER = "manual"
AUTOMATION = "ticket creation"

USECASE = UseCase(
    id=20,
    domain="swe-" + BLOCK,
    title="Break an epic into tickets",
    ask="Split the 'Invoice exports' epic into tickets.",
    why="Creating tickets is a write; the batch is approved, and one ticket is edited before creation.",
    tools=[TOOL("create_ticket", "Create a Jira ticket.", "created", {"title": str, "points": int}, "write")],
    plan=[par(call("create_ticket", title="CSV export endpoint", points=3), call("create_ticket", title="Async export for >10k rows", points=5),
              call("create_ticket", title="Export UI button", points=1)),
          say("Created 3 tickets for the epic (9 points). The async export one was retitled as you asked.")],
    hitl={"create_ticket": ["approve", ("edit", {"title": "Async email export for >10k rows"}), "approve"]},
    expect=[("edited title used", lambda c: any(a["args"]["title"].startswith("Async email") for a in c["world"].actions))]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
