# 050. Price drop after I bought it

**Area:** Bills, budget and money admin  
**Features:** approval

Checks recent orders against current prices and files a price-adjustment request after approval.

## What you ask

> Did anything I bought recently drop in price?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recent_orders"]:::tool
    RT --> S1
    S2["current_price"]:::tool
    S1 --> S2
    S3["request_price_adjustment - approval"]:::appr
    S2 --> S3
    Z(["Answer"])
    S3 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `recent_orders`: Recent orders. | read-only | - |
| `current_price`: Current price of an item. | read-only | - |
| `request_price_adjustment`: Ask a store for a price adjustment. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `request_price_adjustment`: approve

## Run it

```bash
python usecases/050_price_drop_refund/usecase.py                 # your preferred framework
python usecases/050_price_drop_refund/usecase.py --all           # all four frameworks
python usecases/050_price_drop_refund/usecase.py --manual        # answer the approvals yourself
python usecases/050_price_drop_refund/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
