# 123. Running progress

**Area:** Fitness, food and appointments  
**Features:** parallel calls

Reads workout data and compares it with last month.

## What you ask

> How's my running going this month?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["runs"]:::tool
    S2["runs"]:::tool
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
| `runs`: Runs in a month. | read-only | - |

## Run it

```bash
python usecases/123_running_progress/usecase.py                 # your preferred framework
python usecases/123_running_progress/usecase.py --all           # all four frameworks
python usecases/123_running_progress/usecase.py --manual        # answer the approvals yourself
python usecases/123_running_progress/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
