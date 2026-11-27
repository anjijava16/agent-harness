"""Dockerfile size and build-time optimization

When:     12:25 (coding)
Trigger:  manual
Type:     build

Reads the Dockerfile, rewrites it as a multi-stage build, checks size with a tool.

Run:  python usecases/swe_day/037_dockerfile_optimization/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/037_dockerfile_optimization/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "12:25"
BLOCK = "coding"
TRIGGER = "manual"
AUTOMATION = "build"

USECASE = UseCase(
    id=37,
    domain="swe-" + BLOCK,
    title="Dockerfile size and build-time optimization",
    ask="Make the payments-api image smaller.",
    why="Reads the Dockerfile, rewrites it as a multi-stage build, checks size with a tool.",
    tools=[TOOL("image_size", "Build an image and report its size.", {"mb": 210}, {"dockerfile": str})],
    seed_files={"/repo/Dockerfile": "FROM python:3.12\nCOPY . .\nRUN pip install -r requirements.txt\n"},
    plan=[read("/repo/Dockerfile"),
          write("/repo/Dockerfile", "FROM python:3.12-slim AS build\nCOPY requirements.txt .\nRUN pip wheel -r requirements.txt -w /w\n"
                "FROM python:3.12-slim\nCOPY --from=build /w /w\nRUN pip install /w/*\nCOPY . .\n"),
          call("image_size", dockerfile="Dockerfile"),
          say("Multi-stage slim build: image is now 210 MB (was about 1.1 GB with python:3.12).")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
