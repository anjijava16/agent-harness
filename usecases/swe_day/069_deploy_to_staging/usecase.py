"""Deploy to staging

When:     16:20 (release)
Trigger:  webhook: tag.pushed
Type:     deploy

Staging deploys are self-serve; the guard stops the agent pointing the same tool at prod.

Run:  python usecases/swe_day/069_deploy_to_staging/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/069_deploy_to_staging/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "16:20"
BLOCK = "release"
TRIGGER = "webhook: tag.pushed"
AUTOMATION = "deploy"

USECASE = UseCase(
    id=69,
    domain="swe-" + BLOCK,
    title="Deploy to staging",
    ask="Deploy v2.32.0 to staging.",
    why="Staging deploys are self-serve; the guard stops the agent pointing the same tool at prod.",
    tools=[TOOL("deploy", "Deploy a version to an environment.", "deployed", {"service": str, "version": str, "env": str}, "write")],
    plan=[call("deploy", service="payments-api", version="v2.32.0", env="staging"),
          say("v2.32.0 is on staging.")],
    guard={"deploy": lambda a: "prod deploys go through promote_to_prod" if a["env"] == "prod" else None}
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
