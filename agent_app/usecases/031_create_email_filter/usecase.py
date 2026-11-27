"""Make an email filter

Area: inbox
Creates the rule after approval. Rules that delete mail are blocked.

Run:  python usecases/031_create_email_filter/usecase.py                  # your preferred framework
      python usecases/031_create_email_filter/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/031_create_email_filter/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=31,
    area="inbox",
    title="Make an email filter",
    ask="Filter project-alerts into a folder.",
    why="Creates the rule after approval. Rules that delete mail are blocked.",
    tools=[T("create_filter", "Create an email filter.", {"sender": str, "action": str}, "created", "write")],
    steps=[call("create_filter", sender="project-alerts", action="delete"),
           call("create_filter", sender="project-alerts", action="move:Alerts"),
           answer("Filter created: project-alerts goes to the Alerts folder. I didn't make a delete rule; those are blocked.")],
    approvals={"create_filter": "approve"},
    guards={"create_filter": lambda a, p: "filters may not delete mail" if a["action"] == "delete" else None}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
