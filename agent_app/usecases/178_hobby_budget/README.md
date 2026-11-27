# 178. Hobby spending

**Area:** Learning and hobbies  
**Features:** tools only

Totals by hobby.

## What you ask

> How much did I spend on hobbies this year?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["spend_by_tag"]:::tool
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
| `spend_by_tag`: Spending by tag. | read-only | - |

## Run it

```bash
python usecases/178_hobby_budget/usecase.py                 # your preferred framework
python usecases/178_hobby_budget/usecase.py --all           # all four frameworks
python usecases/178_hobby_budget/usecase.py --manual        # answer the approvals yourself
python usecases/178_hobby_budget/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
