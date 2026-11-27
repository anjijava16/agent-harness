"""Ride to the airport

Area: travel
Compares rideshare and train and schedules a ride after approval.

Run:  python usecases/088_airport_ride/usecase.py                  # your preferred framework
      python usecases/088_airport_ride/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/088_airport_ride/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=88,
    area="travel",
    title="Ride to the airport",
    ask="Get me to O'Hare by 6am tomorrow.",
    why="Compares rideshare and train and schedules a ride after approval.",
    tools=[T("ride_quote", "Rideshare quote.", {"from_city": str, "to": str, "arrive_by": str}, {"price": 48, "pickup": "05:15"}),
           T("train_time", "Train time to the airport.", {"arrive_by": str}, {"leave": "04:40", "price": 5}),
           T("schedule_ride", "Schedule a ride.", {"pickup": str, "to": str}, "scheduled", "money")],
    steps=[par(call("ride_quote", from_city="{home_city}", to="ORD", arrive_by="06:00"), call("train_time", arrive_by="06:00")),
           call("schedule_ride", pickup="05:15", to="ORD"),
           answer("Ride scheduled for 5:15 ($48). The train is $5 but you'd have to leave at 4:40.")],
    approvals={"schedule_ride": "approve"}
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
