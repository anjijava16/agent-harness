"""Release readiness checklist

When:     16:10 (release)
Trigger:  manual
Type:     release gate

Checks CI, migrations, open blockers and on-call coverage in parallel, tracked as todos.

Run:  python usecases/swe_day/068_release_readiness_checklist/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/068_release_readiness_checklist/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "16:10"
BLOCK = "release"
TRIGGER = "manual"
AUTOMATION = "release gate"

USECASE = UseCase(
    id=68,
    domain="swe-" + BLOCK,
    title="Release readiness checklist",
    ask="Is v2.32.0 ready to ship?",
    why="Checks CI, migrations, open blockers and on-call coverage in parallel, tracked as todos.",
    tools=[TOOL("ci_status", "CI status for a ref.", "green", {"ref": str}),
           TOOL("open_blockers", "Open release blockers.", [], {"version": str}),
           TOOL("pending_migrations", "Migrations in the release.", ["0043_idempotency_keys (has down)"], {"version": str}),
           TOOL("oncall_now", "Who is on call.", "kai")],
    plan=[todos("CI green", "No blockers", "Migrations reversible", "On-call aware"),
          par(call("ci_status", ref="v2.32.0"), call("open_blockers", version="v2.32.0"),
              call("pending_migrations", version="v2.32.0"), call("oncall_now", query="payments")),
          say("Ready: CI green, no blockers, migration 0043 is reversible, kai is on call.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
