"""Batch my errands into one trip

Area: errands
Orders the stops by opening hours and distance.

Run:  python usecases/074_post_office_trip/usecase.py                  # your preferred framework
      python usecases/074_post_office_trip/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/074_post_office_trip/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=74,
    area="errands",
    title="Batch my errands into one trip",
    ask="I need the post office, pharmacy and hardware store. Best route?",
    why="Orders the stops by opening hours and distance.",
    tools=[T("route", "Best order for stops.", {"stops": str, "city": str}, {"order": ["pharmacy", "hardware", "post office"], "minutes": 48})],
    steps=[call("route", stops="post office, pharmacy, hardware", city="{home_city}"),
           answer("Pharmacy, then hardware store, then the post office: about 48 minutes in total.")]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
