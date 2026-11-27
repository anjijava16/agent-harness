"""Update the team wiki

When:     18:00 (release)
Trigger:  manual
Type:     docs

Small doc updates are easy to skip. This makes them a 30-second task.

Run:  python usecases/swe_day/078_wiki_page_update/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/078_wiki_page_update/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "18:00"
BLOCK = "release"
TRIGGER = "manual"
AUTOMATION = "docs"

USECASE = UseCase(
    id=78,
    domain="swe-" + BLOCK,
    title="Update the team wiki",
    ask="Add today's incident learnings to the checkout runbook page.",
    why="Small doc updates are easy to skip. This makes them a 30-second task.",
    tools=[TOOL("wiki_get", "Get a wiki page.", "## Checkout runbook\n- Check recent deploys\n", {"page": str}),
           TOOL("wiki_update", "Update a wiki page.", "updated", {"page": str, "body": str}, "external")],
    plan=[call("wiki_get", page="checkout-runbook"),
          call("wiki_update", page="checkout-runbook", body="## Checkout runbook\n- Check recent deploys\n- KeyError currency = pricing config missing; roll back\n"),
          say("Checkout runbook updated with the currency KeyError signature.")],
    hitl={"wiki_update": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
