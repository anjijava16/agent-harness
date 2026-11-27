# 053. How much is that in dollars

**Area:** Bills, budget and money admin  
**Features:** uses preferences

Uses the live rate for your currency preference.

## What you ask

> Convert 250 euros for my trip budget.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["fx_rate"]:::tool
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
| `fx_rate`: Exchange rate. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `currency` | USD |

## Run it

```bash
python usecases/053_currency_for_trip/usecase.py                 # your preferred framework
python usecases/053_currency_for_trip/usecase.py --all           # all four frameworks
python usecases/053_currency_for_trip/usecase.py --manual        # answer the approvals yourself
python usecases/053_currency_for_trip/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
