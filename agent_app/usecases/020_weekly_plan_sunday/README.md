# 020. Sunday week-ahead plan

**Area:** Mornings and daily planning  
**Features:** parallel calls, memory

Looks at the whole week, flags crunch days and saves a short plan.

## What you ask

> Plan my week.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["week_calendar"]:::tool
    S2["deadlines"]:::tool
    RT --> S1
    RT --> S2
    S3["remember week_plan"]:::mem
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
| `week_calendar`: Meetings per day this week. | read-only | - |
| `deadlines`: Deadlines this week. | read-only | - |

## Run it

```bash
python usecases/020_weekly_plan_sunday/usecase.py                 # your preferred framework
python usecases/020_weekly_plan_sunday/usecase.py --all           # all four frameworks
python usecases/020_weekly_plan_sunday/usecase.py --manual        # answer the approvals yourself
python usecases/020_weekly_plan_sunday/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
