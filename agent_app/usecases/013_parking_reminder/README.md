# 013. Street cleaning check

**Area:** Mornings and daily planning  
**Features:** memory, uses preferences

Checks the city street-cleaning schedule for your block.

## What you ask

> Do I need to move my car today?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall parking"]:::mem
    RT --> S1
    S2["street_cleaning"]:::tool
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
| `street_cleaning`: Street cleaning for an address. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `home_city` | Chicago |

## Run it

```bash
python usecases/013_parking_reminder/usecase.py                 # your preferred framework
python usecases/013_parking_reminder/usecase.py --all           # all four frameworks
python usecases/013_parking_reminder/usecase.py --manual        # answer the approvals yourself
python usecases/013_parking_reminder/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
