"""Status page update

When:     14:05 (ops)
Trigger:  manual: during incident
Type:     comms

Status page text is public; the draft is edited by a human before it goes out.

Run:  python usecases/swe_day/053_status_page_update/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/053_status_page_update/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "14:05"
BLOCK = "ops"
TRIGGER = "manual: during incident"
AUTOMATION = "comms"

USECASE = UseCase(
    id=53,
    domain="swe-" + BLOCK,
    title="Status page update",
    ask="Post a status page update for the checkout incident.",
    why="Status page text is public; the draft is edited by a human before it goes out.",
    tools=[TOOL("post_status", "Post to the public status page.", "posted", {"component": str, "status": str, "message": str}, "external")],
    plan=[call("post_status", component="Checkout", status="monitoring", message="A recent change caused checkout errors. We rolled it back."),
          say("Status page updated (status: monitoring) with your wording.")],
    hitl={"post_status": ("edit", {"message": "Some checkout attempts failed between 13:18 and 13:41 UTC. A fix is in place and we are monitoring."})},
    expect=[("human wording used", lambda c: "13:18" in c["world"].actions[0]["args"]["message"])]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
