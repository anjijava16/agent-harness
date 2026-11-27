# 147. What's my role worth

**Area:** Work and career  
**Features:** uses preferences

Pulls public salary data for your city.

## What you ask

> What are similar roles paying in my city?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["salary_data"]:::tool
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
| `salary_data`: Public salary ranges. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `home_city` | Chicago |

## Run it

```bash
python usecases/147_job_market_check/usecase.py                 # your preferred framework
python usecases/147_job_market_check/usecase.py --all           # all four frameworks
python usecases/147_job_market_check/usecase.py --manual        # answer the approvals yourself
python usecases/147_job_market_check/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
