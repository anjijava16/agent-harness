"""Today's one goal

Area: mornings
Saves it to long-term memory so the evening review can check it.

Run:  python usecases/018_daily_quote_and_goal/usecase.py                  # your preferred framework
      python usecases/018_daily_quote_and_goal/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/018_daily_quote_and_goal/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=18,
    area="mornings",
    title="Today's one goal",
    ask="Remember my one goal for today: finish the report draft.",
    why="Saves it to long-term memory so the evening review can check it.",
    tools=[],
    steps=[remember("goal_today", "finish the report draft"),
           answer("Saved. Today's goal: finish the report draft. I'll ask about it in your evening review.")],
    expect=[("goal saved", lambda c: c["memories"].get("goal_today") == "finish the report draft")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
