# 115. Dog food running low

**Area:** Home, family and pets  
**Features:** approval, uses preferences

Reads the smart feeder and reorders after approval.

## What you ask

> Are we low on dog food?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["feeder_level"]:::tool
    RT --> S1
    S2["reorder - approval"]:::appr
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
| `feeder_level`: Smart feeder food level. | read-only | - |
| `reorder`: Reorder an item. | spends money | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `reorder`: approve

## Preferences it uses

| Preference | Default |
|---|---|
| `dog` | Biscuit |

## Run it

```bash
python usecases/115_dog_food_reorder/usecase.py                 # your preferred framework
python usecases/115_dog_food_reorder/usecase.py --all           # all four frameworks
python usecases/115_dog_food_reorder/usecase.py --manual        # answer the approvals yourself
python usecases/115_dog_food_reorder/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
