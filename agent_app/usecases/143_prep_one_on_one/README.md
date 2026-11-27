# 143. Prep for my 1:1

**Area:** Work and career  
**Features:** parallel calls, memory

Pulls topics you saved plus wins from the week.

## What you ask

> Prep my 1:1 with my manager.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall 1on1"]:::mem
    S2["week_done"]:::tool
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
| `week_done`: Work finished this week. | read-only | - |

## Run it

```bash
python usecases/143_prep_one_on_one/usecase.py                 # your preferred framework
python usecases/143_prep_one_on_one/usecase.py --all           # all four frameworks
python usecases/143_prep_one_on_one/usecase.py --manual        # answer the approvals yourself
python usecases/143_prep_one_on_one/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
