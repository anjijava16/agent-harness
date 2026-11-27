# 003. Plan my day from my task list

**Area:** Mornings and daily planning  
**Features:** parallel calls, memory, uses preferences

Fits open tasks into calendar gaps inside your work hours, and saves the plan.

## What you ask

> Plan my day around my meetings.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["get_calendar"]:::tool
    S2["open_tasks"]:::tool
    RT --> S1
    RT --> S2
    S3["remember plan_today"]:::mem
    S1 --> S3
    S2 --> S3
    Z(["Answer"])
    S3 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `get_calendar`: Events for a day. | read-only | - |
| `open_tasks`: Open tasks with estimates. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `work_hours` | 09:00-17:30 |

## Run it

```bash
python usecases/003_day_plan_from_tasks/usecase.py                 # your preferred framework
python usecases/003_day_plan_from_tasks/usecase.py --all           # all four frameworks
python usecases/003_day_plan_from_tasks/usecase.py --manual        # answer the approvals yourself
python usecases/003_day_plan_from_tasks/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
