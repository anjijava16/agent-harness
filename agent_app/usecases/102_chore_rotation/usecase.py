"""Weekly chore rotation

Area: home
Rotates from last week's list in memory and posts to the family chat after approval.

Run:  python usecases/102_chore_rotation/usecase.py                  # your preferred framework
      python usecases/102_chore_rotation/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/102_chore_rotation/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=102,
    area="home",
    title="Weekly chore rotation",
    ask="Make this week's chore rotation and send it to the family.",
    why="Rotates from last week's list in memory and posts to the family chat after approval.",
    tools=[T("post_family_chat", "Post to the family chat.", {"text": str}, "posted", "external")],
    steps=[recall("chores"), call("post_family_chat", text="This week: Sam dishes, Jordan laundry, Maya feeds Biscuit."),
           remember("chores", "last week: Sam dishes, Jordan laundry, Maya feeds dog"),
           answer("Rotation posted: Sam on dishes, {partner} on laundry, {kid} feeds {dog}.")],
    approvals={"post_family_chat": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
