# 059. Household expenses with Jordan

**Area:** Bills, budget and money admin  
**Features:** approval, uses preferences

Totals the shared expense log and settles up after approval.

## What you ask

> What do Jordan and I owe each other this month?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["shared_expenses"]:::tool
    RT --> S1
    S2["request_payment - approval"]:::appr
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
| `shared_expenses`: Shared expenses. | read-only | - |
| `request_payment`: Send a payment request. | spends money | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `request_payment`: approve

## Preferences it uses

| Preference | Default |
|---|---|
| `partner` | Jordan |

## Run it

```bash
python usecases/059_shared_expenses/usecase.py                 # your preferred framework
python usecases/059_shared_expenses/usecase.py --all           # all four frameworks
python usecases/059_shared_expenses/usecase.py --manual        # answer the approvals yourself
python usecases/059_shared_expenses/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
