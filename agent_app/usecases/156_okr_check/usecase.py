"""Check my goals

Area: work
Reads goal progress and flags the one at risk.

Run:  python usecases/156_okr_check/usecase.py                  # your preferred framework
      python usecases/156_okr_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/156_okr_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=156,
    area="work",
    title="Check my goals",
    ask="Where am I on my quarterly goals?",
    why="Reads goal progress and flags the one at risk.",
    tools=[T("goals", "Quarterly goals.", {"quarter": str}, [{"goal": "Ship report", "pct": 100}, {"goal": "Cut vendor cost 10%", "pct": 40}])],
    steps=[call("goals", quarter="Q4"), answer("The report goal is done. Cutting vendor cost is at 40%, so that's the one at risk.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
