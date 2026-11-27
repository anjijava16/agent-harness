"""Prep for my 1:1

Area: work
Pulls topics you saved plus wins from the week.

Run:  python usecases/143_prep_one_on_one/usecase.py                  # your preferred framework
      python usecases/143_prep_one_on_one/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/143_prep_one_on_one/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=143,
    area="work",
    title="Prep for my 1:1",
    ask="Prep my 1:1 with my manager.",
    why="Pulls topics you saved plus wins from the week.",
    tools=[T("week_done", "Work finished this week.", {"week": str}, ["Quarterly report shipped"])],
    steps=[par(recall("1on1"), call("week_done", week="this")),
           answer("Talk about the quarterly report shipping, your saved topic (the training budget), and next quarter's goals.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
