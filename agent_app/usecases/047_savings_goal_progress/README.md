# 047. Savings goal progress

**Area:** Bills, budget and money admin  
**Features:** parallel calls, memory

Reads the goal you saved and projects when you'll hit it.

## What you ask

> How's the vacation fund coming along?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall vacation"]:::mem
    S2["goal_progress"]:::tool
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
| `goal_progress`: Progress on a savings goal. | read-only | - |

## Run it

```bash
python usecases/047_savings_goal_progress/usecase.py                 # your preferred framework
python usecases/047_savings_goal_progress/usecase.py --all           # all four frameworks
python usecases/047_savings_goal_progress/usecase.py --manual        # answer the approvals yourself
python usecases/047_savings_goal_progress/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
