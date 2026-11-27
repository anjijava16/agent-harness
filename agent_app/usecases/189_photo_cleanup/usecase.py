"""Clean up blurry photos

Area: digital
Moves them to a review album. It doesn't delete.

Run:  python usecases/189_photo_cleanup/usecase.py                  # your preferred framework
      python usecases/189_photo_cleanup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/189_photo_cleanup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=189,
    area="digital",
    title="Clean up blurry photos",
    ask="Find blurry and duplicate photos from this month.",
    why="Moves them to a review album. It doesn't delete.",
    tools=[T("photo_quality", "Find blurry and duplicate photos.", {"month": str}, {"blurry": 41, "duplicates": 63}),
           T("move_to_album", "Move photos to an album.", {"album": str, "count": int}, "moved", "write")],
    steps=[call("photo_quality", month="this"), call("move_to_album", album="Review: blurry + dupes", count=104),
           answer("104 photos (41 blurry, 63 duplicates) moved to a review album. Nothing was deleted.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
