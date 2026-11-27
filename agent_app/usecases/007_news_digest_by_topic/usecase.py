"""News digest on my topics

Area: mornings
Pulls each topic in parallel. Change news_topics in your preferences and the digest changes with
it.

Run:  python usecases/007_news_digest_by_topic/usecase.py                  # your preferred framework
      python usecases/007_news_digest_by_topic/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/007_news_digest_by_topic/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=7,
    area="mornings",
    title="News digest on my topics",
    ask="Summarize the news for my topics.",
    why="Pulls each topic in parallel. Change news_topics in your preferences and the digest changes with it.",
    tools=[T("search_news", "Latest news for a query.", {"query": str}, lambda query: [f"{query}: 3 stories today"])],
    steps=[par(call("search_news", query="AI"), call("search_news", query="climate"), call("search_news", query="{home_city}")),
           answer("Three stories each on AI, climate and {home_city}. The biggest is the new open model release.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
