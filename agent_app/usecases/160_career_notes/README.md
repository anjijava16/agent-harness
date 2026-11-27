# 160. Brag doc entry

**Area:** Work and career  
**Features:** memory

Saves wins as they happen, so review season is easy.

## What you ask

> Add to my brag doc: led the Q4 review across 4 teams.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["remember brag_q4"]:::mem
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
| (only `remember` / `recall`) | memory | - |

## Run it

```bash
python usecases/160_career_notes/usecase.py                 # your preferred framework
python usecases/160_career_notes/usecase.py --all           # all four frameworks
python usecases/160_career_notes/usecase.py --manual        # answer the approvals yourself
python usecases/160_career_notes/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
