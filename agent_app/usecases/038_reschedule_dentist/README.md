# 038. Reschedule an appointment

**Area:** Email, messages and calendar  
**Features:** parallel calls, approval

Checks open slots against your calendar, then books after approval.

## What you ask

> Move my dentist appointment to next week.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["provider_slots"]:::tool
    S2["get_calendar"]:::tool
    RT --> S1
    RT --> S2
    S3["rebook - approval"]:::appr
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
| `provider_slots`: Open slots at a provider. | read-only | - |
| `get_calendar`: Events for a day. | read-only | - |
| `rebook`: Rebook an appointment. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `rebook`: approve

## Run it

```bash
python usecases/038_reschedule_dentist/usecase.py                 # your preferred framework
python usecases/038_reschedule_dentist/usecase.py --all           # all four frameworks
python usecases/038_reschedule_dentist/usecase.py --manual        # answer the approvals yourself
python usecases/038_reschedule_dentist/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
