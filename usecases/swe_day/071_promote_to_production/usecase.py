"""Promote to production

When:     16:45 (release)
Trigger:  manual
Type:     deploy

The one step that always needs a human.

Run:  python usecases/swe_day/071_promote_to_production/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/071_promote_to_production/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "16:45"
BLOCK = "release"
TRIGGER = "manual"
AUTOMATION = "deploy"

USECASE = UseCase(
    id=71,
    domain="swe-" + BLOCK,
    title="Promote to production",
    ask="Promote v2.32.0 to prod as a 10% canary.",
    why="The one step that always needs a human.",
    tools=[TOOL("promote_to_prod", "Start a prod canary.", "canary started", {"service": str, "version": str, "percent": int}, "money")],
    plan=[call("promote_to_prod", service="payments-api", version="v2.32.0", percent=10),
          say("v2.32.0 canary is live at 10%.")],
    hitl={"promote_to_prod": "approve"}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
