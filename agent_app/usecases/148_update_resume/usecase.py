"""Add a win to my resume

Area: work
Edits your resume doc after you approve the wording.

Run:  python usecases/148_update_resume/usecase.py                  # your preferred framework
      python usecases/148_update_resume/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/148_update_resume/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=148,
    area="work",
    title="Add a win to my resume",
    ask="Add the quarterly report project to my resume.",
    why="Edits your resume doc after you approve the wording.",
    tools=[T("append_resume", "Append a bullet to the resume.", {"section": str, "bullet": str}, "added", "write")],
    steps=[call("append_resume", section="Experience", bullet="Led the Q4 report"),
           answer("The bullet is added to your resume under Experience.")],
    approvals={"append_resume": ("edit", {"bullet": "Led the Q4 business review across 4 teams; cut prep time from 3 weeks to 1"})}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
