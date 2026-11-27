"""Museum visit this weekend

Area: learning
Checks exhibits and free-admission days together.

Run:  python usecases/168_museum_visit/usecase.py                  # your preferred framework
      python usecases/168_museum_visit/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/168_museum_visit/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=168,
    area="learning",
    title="Museum visit this weekend",
    ask="Any good exhibits this weekend, and free days?",
    why="Checks exhibits and free-admission days together.",
    tools=[T("exhibits", "Current exhibits.", {"city": str}, [{"museum": "Art Institute", "show": "Impressionist light"}]),
           T("free_days", "Free admission days.", {"city": str}, {"Art Institute": "Thursday evenings for residents"})],
    steps=[par(call("exhibits", city="{home_city}"), call("free_days", city="{home_city}")),
           answer("The Art Institute has 'Impressionist light'. It's free on Thursday evenings for residents, so go then instead of the weekend.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
