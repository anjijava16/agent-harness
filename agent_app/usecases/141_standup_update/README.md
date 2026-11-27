# 141. Draft my standup update

**Area:** Work and career  
**Features:** parallel calls, memory

Built from yesterday's finished tasks and today's plan.

## What you ask

> Draft my standup update.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["done_tasks"]:::tool
    S2["open_tasks"]:::tool
    S3["recall plan_today"]:::mem
    RT --> S1
    RT --> S2
    RT --> S3
    Z(["Answer"])
    S1 --> Z
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
| `done_tasks`: Tasks done. | read-only | - |
| `open_tasks`: Open tasks. | read-only | - |

## Run it

```bash
python usecases/141_standup_update/usecase.py                 # your preferred framework
python usecases/141_standup_update/usecase.py --all           # all four frameworks
python usecases/141_standup_update/usecase.py --manual        # answer the approvals yourself
python usecases/141_standup_update/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
