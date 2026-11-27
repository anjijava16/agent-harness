# 033. Meeting across time zones

**Area:** Email, messages and calendar  
**Features:** uses preferences

Checks both time zones and suggests sane hours for both of you.

## What you ask

> Find a time for a call with my cousin in Madrid.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["tz_overlap"]:::tool
    RT --> S1
    Z(["Answer"])
    S1 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `tz_overlap`: Overlap of waking hours. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `timezone` | America/Chicago |

## Run it

```bash
python usecases/033_time_zone_meeting/usecase.py                 # your preferred framework
python usecases/033_time_zone_meeting/usecase.py --all           # all four frameworks
python usecases/033_time_zone_meeting/usecase.py --manual        # answer the approvals yourself
python usecases/033_time_zone_meeting/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
