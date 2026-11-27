# 060. Year-end money summary

**Area:** Bills, budget and money admin  
**Features:** parallel calls

Income, spending and savings in parallel, as a short report.

## What you ask

> Give me my money summary for the year.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["totals"]:::tool
    S2["totals"]:::tool
    S3["top_categories"]:::tool
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
| `totals`: Yearly totals. | read-only | - |
| `top_categories`: Top spending categories. | read-only | - |

## Run it

```bash
python usecases/060_year_end_money_summary/usecase.py                 # your preferred framework
python usecases/060_year_end_money_summary/usecase.py --all           # all four frameworks
python usecases/060_year_end_money_summary/usecase.py --manual        # answer the approvals yourself
python usecases/060_year_end_money_summary/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
