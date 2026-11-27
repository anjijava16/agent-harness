# 063. Find the best price

**Area:** Shopping, groceries and errands  
**Features:** parallel calls

Checks several stores at once.

## What you ask

> Where's the cheapest place to buy a 65-inch TV?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["store_price"]:::tool
    S2["store_price"]:::tool
    S3["store_price"]:::tool
    RT --> S1
    RT --> S2
    RT --> S3
    Z(["Answer"])
    S1 --> Z
    S2 --> Z
    S3 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `store_price`: Price at a store. | read-only | - |

## Run it

```bash
python usecases/063_price_compare/usecase.py                 # your preferred framework
python usecases/063_price_compare/usecase.py --all           # all four frameworks
python usecases/063_price_compare/usecase.py --manual        # answer the approvals yourself
python usecases/063_price_compare/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
