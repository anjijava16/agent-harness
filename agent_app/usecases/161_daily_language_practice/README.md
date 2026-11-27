# 161. Daily Spanish practice

**Area:** Learning and hobbies  
**Features:** memory

Picks up where you left off (saved in memory) and saves progress.

## What you ask

> Give me today's Spanish practice.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall spanish"]:::mem
    RT --> S1
    S2["lesson"]:::tool
    S1 --> S2
    S3["remember spanish"]:::mem
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
| `lesson`: Next lesson for a level. | read-only | - |

## Run it

```bash
python usecases/161_daily_language_practice/usecase.py                 # your preferred framework
python usecases/161_daily_language_practice/usecase.py --all           # all four frameworks
python usecases/161_daily_language_practice/usecase.py --manual        # answer the approvals yourself
python usecases/161_daily_language_practice/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
