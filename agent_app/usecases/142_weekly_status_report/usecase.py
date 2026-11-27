"""Weekly status report

Area: work
Collects the week's work and sends it after you edit it.

Run:  python usecases/142_weekly_status_report/usecase.py                  # your preferred framework
      python usecases/142_weekly_status_report/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/142_weekly_status_report/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=142,
    area="work",
    title="Weekly status report",
    ask="Write my weekly status report and send it to my manager.",
    why="Collects the week's work and sends it after you edit it.",
    tools=[T("week_done", "Work finished this week.", {"week": str}, ["Quarterly report", "Vendor shortlist"]),
           T("send_email", "Send an email.", {"to": str, "body": str}, "sent", "external")],
    steps=[call("week_done", week="this"), call("send_email", to="manager", body="Done: quarterly report, vendor shortlist."),
           answer("Status report sent to your manager.")],
    approvals={"send_email": ("edit", {"body": "Done: quarterly report, vendor shortlist. Next week: contract review. Risk: legal turnaround."})}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
