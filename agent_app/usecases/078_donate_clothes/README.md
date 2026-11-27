# 078. Schedule a donation pickup

**Area:** Shopping, groceries and errands  
**Features:** approval

Books a charity pickup after approval.

## What you ask

> Schedule a pickup for two bags of clothes.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["pickup_slots"]:::tool
    RT --> S1
    S2["schedule_pickup - approval"]:::appr
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
| `pickup_slots`: Donation pickup slots. | read-only | - |
| `schedule_pickup`: Book a pickup. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `schedule_pickup`: approve

## Run it

```bash
python usecases/078_donate_clothes/usecase.py                 # your preferred framework
python usecases/078_donate_clothes/usecase.py --all           # all four frameworks
python usecases/078_donate_clothes/usecase.py --manual        # answer the approvals yourself
python usecases/078_donate_clothes/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
