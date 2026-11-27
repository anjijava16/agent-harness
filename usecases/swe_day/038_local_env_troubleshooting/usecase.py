"""Local environment troubleshooting

When:     12:28 (coding)
Trigger:  manual
Type:     troubleshooting

Reads the error and compose file, finds the conflict, suggests the exact fix.

Run:  python usecases/swe_day/038_local_env_troubleshooting/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/038_local_env_troubleshooting/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "12:28"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "troubleshooting"

USECASE = UseCase(
    id=38,
    domain="swe-" + BLOCK,
    title="Local environment troubleshooting",
    ask="docker compose up fails on my machine. Help.",
    why="Reads the error and compose file, finds the conflict, suggests the exact fix.",
    tools=[TOOL("compose_logs", "docker compose logs.", "Error: bind for 0.0.0.0:5432 failed: port is already allocated", {"service": str})],
    seed_files={"/repo/docker-compose.yml": "services:\n  db:\n    image: postgres:16\n    ports: ['5432:5432']\n"},
    plan=[call("compose_logs", service="db"), read("/repo/docker-compose.yml"),
          say("Port 5432 is already used, probably by a local Postgres. Stop it (brew services stop postgresql) or map '5433:5432' in compose.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
