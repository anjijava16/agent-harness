# 030. Who emails me most

**Area:** Email, messages and calendar  
**Features:** tools only

Stats on the last 30 days.

## What you ask

> Who takes most of my email time?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["email_stats"]:::tool
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
| `email_stats`: Email volume by sender. | read-only | - |

## Run it

```bash
python usecases/030_weekly_email_report/usecase.py                 # your preferred framework
python usecases/030_weekly_email_report/usecase.py --all           # all four frameworks
python usecases/030_weekly_email_report/usecase.py --manual        # answer the approvals yourself
python usecases/030_weekly_email_report/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
