"""Find flights

Area: travel
Searches with your seat preference and shows the best options.

Run:  python usecases/082_flight_search/usecase.py                  # your preferred framework
      python usecases/082_flight_search/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/082_flight_search/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=82,
    area="travel",
    title="Find flights",
    ask="Find flights to Denver for Dec 12-15.",
    why="Searches with your seat preference and shows the best options.",
    tools=[T("search_flights", "Search flights.", {"origin": str, "dest": str, "dates": str, "seat": str},
             [{"airline": "United", "price": 248, "depart": "07:10", "seat": "aisle available"}, {"airline": "Southwest", "price": 219, "depart": "13:40"}])],
    steps=[call("search_flights", origin="ORD", dest="DEN", dates="Dec 12-15", seat="{seat_preference}"),
           answer("Southwest at 13:40 for $219 is the cheapest. United at 07:10 is $248 and has {seat_preference} seats.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
