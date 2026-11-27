"""Share an event with family

Area: inbox
Copying events to someone else's calendar needs approval.

Run:  python usecases/035_share_calendar_family/usecase.py                  # your preferred framework
      python usecases/035_share_calendar_family/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/035_share_calendar_family/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=35,
    area="inbox",
    title="Share an event with family",
    ask="Add Maya's recital to Jordan's calendar too.",
    why="Copying events to someone else's calendar needs approval.",
    tools=[T("find_event", "Find an event.", {"query": str}, {"id": "e77", "title": "Maya recital", "when": "Thu 17:00"}),
           T("share_event", "Share an event with someone.", {"event_id": str, "with_person": str}, "shared", "external")],
    steps=[call("find_event", query="recital"), call("share_event", event_id="e77", with_person="{partner}"),
           answer("{kid}'s recital (Thu 17:00) is now on {partner}'s calendar.")],
    approvals={"share_event": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
