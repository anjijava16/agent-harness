"""Hotel shortlist

Area: travel
Searches and filters by price and distance.

Run:  python usecases/084_hotel_shortlist/usecase.py                  # your preferred framework
      python usecases/084_hotel_shortlist/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/084_hotel_shortlist/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=84,
    area="travel",
    title="Hotel shortlist",
    ask="Hotels near the conference center in Denver under $200?",
    why="Searches and filters by price and distance.",
    tools=[T("search_hotels", "Search hotels.", {"city": str, "near": str, "max_price": int}, [{"name": "Maven", "price": 189, "walk_min": 6}, {"name": "Hyatt Place", "price": 165, "walk_min": 12}])],
    steps=[call("search_hotels", city="Denver", near="convention center", max_price=200),
           answer("The Maven: $189, 6 minutes' walk. Hyatt Place: $165, 12 minutes. Both are under $200.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
