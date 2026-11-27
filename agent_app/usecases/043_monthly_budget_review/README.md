# 043. Monthly budget review

**Area:** Bills, budget and money admin  
**Features:** parallel calls

Compares spending by category with the budget you set.

## What you ask

> How did I do against my budget this month?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["spending_by_category"]:::tool
    S2["budget"]:::tool
    RT --> S1
    RT --> S2
    Z(["Answer"])
    S1 --> Z
    S2 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `spending_by_category`: Spending this month. | read-only | - |
| `budget`: Your budget. | read-only | - |

## Run it

```bash
python usecases/043_monthly_budget_review/usecase.py                 # your preferred framework
python usecases/043_monthly_budget_review/usecase.py --all           # all four frameworks
python usecases/043_monthly_budget_review/usecase.py --manual        # answer the approvals yourself
python usecases/043_monthly_budget_review/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
