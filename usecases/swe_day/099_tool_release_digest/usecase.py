"""Weekly digest of tool releases

When:     23:58 (night)
Trigger:  cron: 58 23 * * 0
Type:     learning

Two researcher subagents read release notes; you get the 3 lines that matter.

Run:  python usecases/swe_day/099_tool_release_digest/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/099_tool_release_digest/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "23:58"
BLOCK = "night"
TRIGGER = "cron: 58 23 * * 0"
AUTOMATION = "learning"

USECASE = UseCase(
    id=99,
    domain="swe-" + BLOCK,
    title="Weekly digest of tool releases",
    ask="What changed this week in the tools we use?",
    why="Two researcher subagents read release notes; you get the 3 lines that matter.",
    tools=[TOOL("release_notes", "Latest release notes for a project.", lambda project: {"deepagents": "0.7.x: subagent streaming, async backends",
                                                                                         "fastapi": "0.120: dependency caching changes"}[project], {"project": str})],
    subagents=[SUB("agents-reader", "Reads agent framework releases.", ["release_notes"], [call("release_notes", project="deepagents"), say("deepagents: subagent streaming, async backends.")]),
               SUB("web-reader", "Reads web framework releases.", ["release_notes"], [call("release_notes", project="fastapi"), say("fastapi 0.120 changed dependency caching. Check our Depends usage.")])],
    plan=[par(task("agents-reader", "What's new in deepagents this week?"), task("web-reader", "What's new in fastapi this week?")),
          say("This week: deepagents added subagent streaming; FastAPI 0.120 changed dependency caching, which is worth a look before upgrading.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
