# 027. Decline a meeting politely

**Area:** Email, messages and calendar  
**Features:** approval, memory

Uses your saved tone preference from memory.

## What you ask

> Decline Friday's optional all-hands and say why.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall tone"]:::mem
    RT --> S1
    S2["rsvp - approval"]:::appr
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
| `rsvp`: RSVP to an event. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `rsvp`: approve

## Run it

```bash
python usecases/027_decline_politely/usecase.py                 # your preferred framework
python usecases/027_decline_politely/usecase.py --all           # all four frameworks
python usecases/027_decline_politely/usecase.py --manual        # answer the approvals yourself
python usecases/027_decline_politely/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
