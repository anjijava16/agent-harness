# 006. School run check

**Area:** Mornings and daily planning  
**Features:** parallel calls, memory, uses preferences

Reads the school portal and your memory of what she needs on gym days.

## What you ask

> Anything I need for Maya's school today?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["school_notices"]:::tool
    S2["recall gym"]:::mem
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
| `school_notices`: Notices from the school portal. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `kid` | Maya |

## Run it

```bash
python usecases/006_school_run_check/usecase.py                 # your preferred framework
python usecases/006_school_run_check/usecase.py --all           # all four frameworks
python usecases/006_school_run_check/usecase.py --manual        # answer the approvals yourself
python usecases/006_school_run_check/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
