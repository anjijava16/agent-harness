"""Close tickets that shipped

When:     17:20 (release)
Trigger:  webhook: release.published
Type:     ticket hygiene

Moving tickets is a write; done in one approved batch.

Run:  python usecases/swe_day/074_close_shipped_tickets/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/074_close_shipped_tickets/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "17:20"
BLOCK = "release"
TRIGGER = "webhook: release.published"
AUTOMATION = "ticket hygiene"

USECASE = UseCase(
    id=74,
    domain="swe-" + BLOCK,
    title="Close tickets that shipped",
    ask="Close the Jira tickets included in v2.32.0.",
    why="Moving tickets is a write; done in one approved batch.",
    tools=[TOOL("tickets_in_release", "Tickets linked to a release.", ["PAY-431", "PAY-440"], {"version": str}),
           TOOL("transition_ticket", "Move a ticket to a status.", "done", {"key": str, "status": str}, "write")],
    plan=[call("tickets_in_release", version="v2.32.0"),
          par(call("transition_ticket", key="PAY-431", status="Done"), call("transition_ticket", key="PAY-440", status="Done")),
          say("PAY-431 and PAY-440 moved to Done.")],
    hitl={"transition_ticket": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
