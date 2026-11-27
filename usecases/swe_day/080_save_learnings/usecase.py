"""Save today's learnings

When:     18:20 (release)
Trigger:  manual
Type:     knowledge

Writes to /memories/, which persists across threads, so the incident agent knows next
time.

Run:  python usecases/swe_day/080_save_learnings/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/080_save_learnings/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "18:20"
BLOCK = "release"
TRIGGER = "manual"
AUTOMATION = "knowledge"

USECASE = UseCase(
    id=80,
    domain="swe-" + BLOCK,
    title="Save today's learnings",
    ask="Remember: pricing config KeyError means the currency map is missing; rollback, then fix config.",
    why="Writes to /memories/, which persists across threads, so the incident agent knows next time.",
    tools=[],
    long_term_memory=True,
    plan=[write("/memories/learnings.md", "- KeyError currency in pricing.py = missing currency map. Roll back first, fix config after.\n"),
          say("Saved. The triage agent will see it next time.")],
    expect=[("learning persisted", lambda c: "learnings.md" in " ".join(c["store_keys"]))]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
