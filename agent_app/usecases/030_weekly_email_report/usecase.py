"""Who emails me most

Area: inbox
Stats on the last 30 days.

Run:  python usecases/030_weekly_email_report/usecase.py                  # your preferred framework
      python usecases/030_weekly_email_report/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/030_weekly_email_report/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=30,
    area="inbox",
    title="Who emails me most",
    ask="Who takes most of my email time?",
    why="Stats on the last 30 days.",
    tools=[T("email_stats", "Email volume by sender.", {"days": int}, [{"sender": "project-alerts", "count": 410}, {"sender": "boss", "count": 52}])],
    steps=[call("email_stats", days=30),
           answer("project-alerts sent 410 emails in 30 days. A filter into a folder would clear most of it.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
