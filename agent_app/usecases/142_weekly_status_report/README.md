# 142. Weekly status report

**Area:** Work and career  
**Features:** approval

Collects the week's work and sends it after you edit it.

## What you ask

> Write my weekly status report and send it to my manager.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["week_done"]:::tool
    RT --> S1
    S2["send_email - approval"]:::appr
    S1 --> S2
    Z(["Answer"])
    S2 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `week_done`: Work finished this week. | read-only | - |
| `send_email`: Send an email. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `send_email`: approve with edits `body='Done: quarterly report, vendor shortlist. Next week: contract review. Risk: legal turnaround.'`

## Run it

```bash
python usecases/142_weekly_status_report/usecase.py                 # your preferred framework
python usecases/142_weekly_status_report/usecase.py --all           # all four frameworks
python usecases/142_weekly_status_report/usecase.py --manual        # answer the approvals yourself
python usecases/142_weekly_status_report/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
