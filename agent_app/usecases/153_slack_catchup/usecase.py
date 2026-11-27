"""Catch up on Slack after a day off

Area: work
Summarizes mentions and decisions.

Run:  python usecases/153_slack_catchup/usecase.py                  # your preferred framework
      python usecases/153_slack_catchup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/153_slack_catchup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=153,
    area="work",
    title="Catch up on Slack after a day off",
    ask="What did I miss on Slack yesterday?",
    why="Summarizes mentions and decisions.",
    tools=[T("slack_mentions", "Mentions and threads.", {"since": str}, [{"channel": "#launch", "text": "Launch moved to Dec 9"}, {"channel": "#team", "text": "Sam, can you review the deck?"}])],
    steps=[call("slack_mentions", since="yesterday"),
           answer("The launch moved to Dec 9, and someone asked you to review the deck in #team.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
