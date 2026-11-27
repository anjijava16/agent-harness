# 073. What's open near me

**Area:** Shopping, groceries and errands  
**Features:** uses preferences

Checks hours and how busy it is.

## What you ask

> Is the hardware store open now?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["place_hours"]:::tool
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
| `place_hours`: Opening hours. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `home_city` | Chicago |

## Run it

```bash
python usecases/073_find_open_now/usecase.py                 # your preferred framework
python usecases/073_find_open_now/usecase.py --all           # all four frameworks
python usecases/073_find_open_now/usecase.py --manual        # answer the approvals yourself
python usecases/073_find_open_now/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
