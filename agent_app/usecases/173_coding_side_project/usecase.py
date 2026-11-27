"""Side project: what's next

Area: learning
Reads the issue list and your notes, then picks one task.

Run:  python usecases/173_coding_side_project/usecase.py                  # your preferred framework
      python usecases/173_coding_side_project/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/173_coding_side_project/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=173,
    area="learning",
    title="Side project: what's next",
    ask="What's next on my side project?",
    why="Reads the issue list and your notes, then picks one task.",
    tools=[T("open_issues", "Open issues in a repo.", {"repo": str}, [{"n": 12, "title": "Add dark mode", "labels": ["good first"]}, {"n": 15, "title": "Fix login bug", "labels": ["bug"]}])],
    steps=[par(call("open_issues", repo="me/recipe-app"), recall("side_project")),
           answer("Fix the login bug (#15) first. Dark mode can wait.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
