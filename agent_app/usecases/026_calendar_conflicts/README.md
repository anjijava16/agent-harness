# 026. Calendar conflicts

**Area:** Email, messages and calendar  
**Features:** parallel calls, uses preferences

Checks work and family calendars together.

## What you ask

> Any double bookings this week?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["events"]:::tool
    S2["events"]:::tool
    RT --> S1
    RT --> S2
    Z(["Answer"])
    S1 --> Z
    S2 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `events`: Events in a calendar. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `kid` | Maya |

## Run it

```bash
python usecases/026_calendar_conflicts/usecase.py                 # your preferred framework
python usecases/026_calendar_conflicts/usecase.py --all           # all four frameworks
python usecases/026_calendar_conflicts/usecase.py --manual        # answer the approvals yourself
python usecases/026_calendar_conflicts/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
