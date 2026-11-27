# 171. Plan the spring garden

**Area:** Learning and hobbies  
**Features:** memory

Uses your growing zone and what grew well last year (saved in memory).

## What you ask

> What should I plant this spring?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall garden"]:::mem
    RT --> S1
    S2["planting_calendar"]:::tool
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
| `planting_calendar`: Planting calendar for a zone. | read-only | - |

## Run it

```bash
python usecases/171_garden_plan/usecase.py                 # your preferred framework
python usecases/171_garden_plan/usecase.py --all           # all four frameworks
python usecases/171_garden_plan/usecase.py --manual        # answer the approvals yourself
python usecases/171_garden_plan/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
