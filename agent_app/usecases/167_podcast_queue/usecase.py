"""Podcasts for my commute

Area: learning
Picks episodes that fit your commute time and topics.

Run:  python usecases/167_podcast_queue/usecase.py                  # your preferred framework
      python usecases/167_podcast_queue/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/167_podcast_queue/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=167,
    area="learning",
    title="Podcasts for my commute",
    ask="Queue podcasts for tomorrow's commute.",
    why="Picks episodes that fit your commute time and topics.",
    tools=[T("drive_time", "Commute time.", {"city": str}, {"minutes": 34}),
           T("podcast_search", "Episodes by topic and length.", {"topics": str, "max_min": int}, ["AI weekly: 31 min"]),
           T("queue_episode", "Add to queue.", {"episode": str}, "queued", "write")],
    steps=[call("drive_time", city="{home_city}"), call("podcast_search", topics="{news_topics}", max_min=34), call("queue_episode", episode="AI weekly: 31 min"),
           answer("Queued a 31-minute episode of AI weekly for your 34-minute commute.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
