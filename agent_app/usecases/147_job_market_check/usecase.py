"""What's my role worth

Area: work
Pulls public salary data for your city.

Run:  python usecases/147_job_market_check/usecase.py                  # your preferred framework
      python usecases/147_job_market_check/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/147_job_market_check/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=147,
    area="work",
    title="What's my role worth",
    ask="What are similar roles paying in my city?",
    why="Pulls public salary data for your city.",
    tools=[T("salary_data", "Public salary ranges.", {"role": str, "city": str}, {"p25": 118000, "p50": 136000, "p75": 158000})],
    steps=[call("salary_data", role="product manager", city="{home_city}"),
           answer("Product manager in {home_city}: median $136k, middle half $118k to $158k (public postings).")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
