"""Make a photo album

Area: home
Picks the photos by date. Sharing needs approval.

Run:  python usecases/114_family_photos_album/usecase.py                  # your preferred framework
      python usecases/114_family_photos_album/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/114_family_photos_album/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=114,
    area="home",
    title="Make a photo album",
    ask="Make an album of Thanksgiving photos and share it with family.",
    why="Picks the photos by date. Sharing needs approval.",
    tools=[T("photos", "Photos by date.", {"date": str}, {"count": 86}),
           T("create_album", "Create an album.", {"name": str, "date": str}, {"album": "a1"}, "write"),
           T("share_album", "Share an album.", {"album": str, "with_group": str}, "shared", "external")],
    steps=[call("photos", date="Nov 26"), call("create_album", name="Thanksgiving 2026", date="Nov 26"), call("share_album", album="a1", with_group="family"),
           answer("Album 'Thanksgiving 2026' (86 photos) is shared with the family.")],
    approvals={"share_album": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
