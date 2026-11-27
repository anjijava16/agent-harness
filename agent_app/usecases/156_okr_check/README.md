# 156. Check my goals

**Area:** Work and career  
**Features:** tools only

Reads goal progress and flags the one at risk.

## What you ask

> Where am I on my quarterly goals?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["goals"]:::tool
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
| `goals`: Quarterly goals. | read-only | - |

## Run it

```bash
python usecases/156_okr_check/usecase.py                 # your preferred framework
python usecases/156_okr_check/usecase.py --all           # all four frameworks
python usecases/156_okr_check/usecase.py --manual        # answer the approvals yourself
python usecases/156_okr_check/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
