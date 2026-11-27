"""Morning brief

Area: mornings
Calendar, weather and news in parallel, shaped by your city and topics.

Run:  python usecases/001_morning_brief/usecase.py                  # your preferred framework
      python usecases/001_morning_brief/usecase.py --all            # Deep Agents, LangGraph, ADK and Claude Agent SDK
      python usecases/001_morning_brief/usecase.py --manual         # you answer the approvals
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.spec import T, UseCase, answer, call, par, recall, remember  # noqa: E402,F401

USECASE = UseCase(
    id=1,
    area="mornings",
    title="Morning brief",
    ask="Give me my morning brief.",
    why="Calendar, weather and news in parallel, shaped by your city and topics.",
    tools=[T("get_calendar", "Events for a day.", {"day": str}, [{"time": "09:30", "title": "Team standup"}, {"time": "13:00", "title": "Dentist"}]),
           T("get_weather", "Weather for a city.", {"city": str}, lambda city: {"city": city, "high_f": 41, "rain": "60% after 3pm"}),
           T("get_headlines", "Top headlines for topics.", {"topics": str}, ["New open model tops coding benchmark", "Lake Michigan ice cover at record low"])],
    steps=[par(call("get_calendar", day="today"), call("get_weather", city="{home_city}"), call("get_headlines", topics="{news_topics}")),
           answer("Morning, {name}. Standup at 9:30 and the dentist at 1. {home_city}: 41F, rain likely after 3, so take an umbrella. Two headlines picked for your topics.")],
    expect=[("weather for home city", lambda c: any(x["args"].get("city") == c["prefs"]["home_city"] for x in c["calls"]))]
)

if __name__ == "__main__":
    from app.cli import main

    main(USECASE)
