"""Catch up on the family group chat

Area: inbox
Summarizes 140 messages into what you actually need to know.

Run:  python usecases/028_group_chat_catchup/usecase.py                  # your preferred framework
      python usecases/028_group_chat_catchup/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/028_group_chat_catchup/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=28,
    area="inbox",
    title="Catch up on the family group chat",
    ask="What did I miss in the family chat?",
    why="Summarizes 140 messages into what you actually need to know.",
    tools=[T("chat_history", "Messages from a chat.", {"chat": str, "since": str}, {"count": 140, "key": ["Thanksgiving at Rosa's, 3pm", "bring a dessert", "Grandpa's flight lands Wed 6pm"]})],
    steps=[call("chat_history", chat="family", since="2 days"),
           answer("Thanksgiving is at Rosa's at 3pm and you're on dessert. Grandpa lands Wednesday at 6pm.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
