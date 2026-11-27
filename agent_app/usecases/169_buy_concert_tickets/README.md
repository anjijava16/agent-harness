# 169. Concert tickets

**Area:** Learning and hobbies  
**Features:** approval, guard

A purchase with approval, inside your limit.

## What you ask

> Get 2 tickets for the jazz show Friday.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["ticket_price"]:::tool
    RT --> S1
    S2["buy_tickets - approval, guard"]:::appr
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
| `ticket_price`: Ticket price. | read-only | - |
| `buy_tickets`: Buy tickets. | spends money | approval, guard |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `buy_tickets`: approve

## Guards

Checked in the shared tool layer before the tool runs, the same on every framework. Guards get your preferences, so changing a limit in the UI changes what's allowed.

- `buy_tickets`

## Run it

```bash
python usecases/169_buy_concert_tickets/usecase.py                 # your preferred framework
python usecases/169_buy_concert_tickets/usecase.py --all           # all four frameworks
python usecases/169_buy_concert_tickets/usecase.py --manual        # answer the approvals yourself
python usecases/169_buy_concert_tickets/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
