# 105. Homework check

**Area:** Home, family and pets  
**Features:** uses preferences

Reads the school portal and tells you only what's due.

## What you ask

> Does Maya have homework due tomorrow?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["assignments"]:::tool
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
| `assignments`: Assignments due. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `kid` | Maya |

## Run it

```bash
python usecases/105_kid_homework_check/usecase.py                 # your preferred framework
python usecases/105_kid_homework_check/usecase.py --all           # all four frameworks
python usecases/105_kid_homework_check/usecase.py --manual        # answer the approvals yourself
python usecases/105_kid_homework_check/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
