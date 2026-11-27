# 108. Guest access for the dog walker

**Area:** Home, family and pets  
**Features:** approval, guard

Time-limited codes are allowed. Permanent codes are blocked.

## What you ask

> Give the dog walker a door code for weekdays at noon.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["create_door_code - approval, guard"]:::appr
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
| `create_door_code`: Create a door code. | changes your data | approval, guard |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `create_door_code`: approve

## Guards

Checked in the shared tool layer before the tool runs, the same on every framework. Guards get your preferences, so changing a limit in the UI changes what's allowed.

- `create_door_code`

## Run it

```bash
python usecases/108_smart_lock_guest/usecase.py                 # your preferred framework
python usecases/108_smart_lock_guest/usecase.py --all           # all four frameworks
python usecases/108_smart_lock_guest/usecase.py --manual        # answer the approvals yourself
python usecases/108_smart_lock_guest/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
