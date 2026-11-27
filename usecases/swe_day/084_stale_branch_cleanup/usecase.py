"""Stale branch cleanup

When:     20:30 (night)
Trigger:  cron: 30 20 * * 0
Type:     repo hygiene

Runs weekly. Protected branches are blocked by policy no matter what the model decides.

Run:  python usecases/swe_day/084_stale_branch_cleanup/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/084_stale_branch_cleanup/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "20:30"
BLOCK = "night"
TRIGGER = "cron: 30 20 * * 0"
AUTOMATION = "repo hygiene"

USECASE = UseCase(
    id=84,
    domain="swe-" + BLOCK,
    title="Stale branch cleanup",
    ask="Delete merged branches older than 30 days.",
    why="Runs weekly. Protected branches are blocked by policy no matter what the model decides.",
    tools=[TOOL("stale_branches", "Merged branches older than N days.", ["feature/PAY-300", "release/2026.10", "fix/rounding"], {"days": int}),
           TOOL("delete_branch", "Delete a remote branch.", "deleted", {"name": str}, "write")],
    plan=[call("stale_branches", days=30),
          par(call("delete_branch", name="feature/PAY-300"), call("delete_branch", name="release/2026.10"), call("delete_branch", name="fix/rounding")),
          say("Deleted 2 stale branches. release/2026.10 is protected and was kept.")],
    guard={"delete_branch": lambda a: "protected branch" if a["name"].startswith(("release/", "main")) else None},
    expect=[("release branch kept", lambda c: all(not x["args"]["name"].startswith("release/") for x in c["world"].actions))]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
