# 137. Order healthy snacks for the office

**Area:** Fitness, food and appointments  
**Features:** approval, guard

Small purchase, within your limit, with approval.

## What you ask

> Order snacks for my desk.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["checkout - approval, guard"]:::appr
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
| `checkout`: Place an order. | spends money | approval, guard |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `checkout`: approve

## Guards

Checked in the shared tool layer before the tool runs, the same on every framework. Guards get your preferences, so changing a limit in the UI changes what's allowed.

- `checkout`

## Run it

```bash
python usecases/137_healthy_snacks_order/usecase.py                 # your preferred framework
python usecases/137_healthy_snacks_order/usecase.py --all           # all four frameworks
python usecases/137_healthy_snacks_order/usecase.py --manual        # answer the approvals yourself
python usecases/137_healthy_snacks_order/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
