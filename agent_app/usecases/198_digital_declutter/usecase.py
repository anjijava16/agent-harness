"""Monthly digital declutter

Area: digital
Checks downloads, the desktop and old screenshots in parallel. Report only.

Run:  python usecases/198_digital_declutter/usecase.py                  # your preferred framework
      python usecases/198_digital_declutter/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/198_digital_declutter/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=198,
    area="digital",
    title="Monthly digital declutter",
    ask="Do my monthly digital declutter.",
    why="Checks downloads, the desktop and old screenshots in parallel. Report only.",
    tools=[T("folder_stats", "Folder size and file count.", {"folder": str}, lambda folder: {"Downloads": {"files": 212, "gb": 18}, "Desktop": {"files": 44, "gb": 2}, "Screenshots": {"files": 390, "gb": 3}}[folder])],
    steps=[par(call("folder_stats", folder="Downloads"), call("folder_stats", folder="Desktop"), call("folder_stats", folder="Screenshots")),
           answer("Downloads has 212 files (18 GB) and Screenshots has 390. Start with Downloads.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
