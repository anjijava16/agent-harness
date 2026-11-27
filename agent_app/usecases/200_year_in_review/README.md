# 200. My year in review

**Area:** Documents, accounts and digital life  
**Features:** parallel calls, memory

Pulls from money, fitness, learning and memory for one look back at the year.

## What you ask

> Give me my year in review.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["totals"]:::tool
    S2["totals"]:::tool
    S3["totals"]:::tool
    S4["recall brag"]:::mem
    RT --> S1
    RT --> S2
    RT --> S3
    RT --> S4
    Z(["Answer"])
    S1 --> Z
    S2 --> Z
    S3 --> Z
    S4 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `totals`: Yearly totals. | read-only | - |

## Run it

```bash
python usecases/200_year_in_review/usecase.py                 # your preferred framework
python usecases/200_year_in_review/usecase.py --all           # all four frameworks
python usecases/200_year_in_review/usecase.py --manual        # answer the approvals yourself
python usecases/200_year_in_review/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
