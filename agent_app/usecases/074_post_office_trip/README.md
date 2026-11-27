# 074. Batch my errands into one trip

**Area:** Shopping, groceries and errands  
**Features:** uses preferences

Orders the stops by opening hours and distance.

## What you ask

> I need the post office, pharmacy and hardware store. Best route?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["route"]:::tool
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
| `route`: Best order for stops. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `home_city` | Chicago |

## Run it

```bash
python usecases/074_post_office_trip/usecase.py                 # your preferred framework
python usecases/074_post_office_trip/usecase.py --all           # all four frameworks
python usecases/074_post_office_trip/usecase.py --manual        # answer the approvals yourself
python usecases/074_post_office_trip/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
