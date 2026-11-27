# 110. Get the plumber in

**Area:** Home, family and pets  
**Features:** approval, memory

Uses the plumber you saved and texts him after approval.

## What you ask

> The kitchen sink is leaking. Get the plumber.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall plumber"]:::mem
    RT --> S1
    S2["send_sms - approval"]:::appr
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
| `send_sms`: Send a text. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `send_sms`: approve

## Run it

```bash
python usecases/110_plumber_quote/usecase.py                 # your preferred framework
python usecases/110_plumber_quote/usecase.py --all           # all four frameworks
python usecases/110_plumber_quote/usecase.py --manual        # answer the approvals yourself
python usecases/110_plumber_quote/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
