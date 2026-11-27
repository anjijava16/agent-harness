# 054. Collect donation receipts

**Area:** Bills, budget and money admin  
**Features:** memory

Searches email, totals the amounts and saves the list for tax time.

## What you ask

> Gather my donation receipts for the year.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["search_receipts"]:::tool
    RT --> S1
    S2["remember tax_donations_2026"]:::mem
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
| `search_receipts`: Search email receipts. | read-only | - |

## Run it

```bash
python usecases/054_donation_receipts/usecase.py                 # your preferred framework
python usecases/054_donation_receipts/usecase.py --all           # all four frameworks
python usecases/054_donation_receipts/usecase.py --manual        # answer the approvals yourself
python usecases/054_donation_receipts/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
