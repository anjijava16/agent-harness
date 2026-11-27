# 040. Clear out stale recurring meetings

**Area:** Email, messages and calendar  
**Features:** parallel calls, approval

Finds recurring meetings you skip and declines them after approval; one you keep.

## What you ask

> Which recurring meetings could I drop?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recurring_attendance"]:::tool
    RT --> S1
    S2["leave_series - approval"]:::appr
    S3["leave_series - approval"]:::appr
    S1 --> S2
    S1 --> S3
    Z(["Answer"])
    S2 --> Z
    S3 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `recurring_attendance`: Your attendance at recurring meetings. | read-only | - |
| `leave_series`: Leave a recurring meeting. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `leave_series`: call 1: approve; call 2: reject

## Run it

```bash
python usecases/040_weekly_calendar_cleanup/usecase.py                 # your preferred framework
python usecases/040_weekly_calendar_cleanup/usecase.py --all           # all four frameworks
python usecases/040_weekly_calendar_cleanup/usecase.py --manual        # answer the approvals yourself
python usecases/040_weekly_calendar_cleanup/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
