# 153. Catch up on Slack after a day off

**Area:** Work and career  
**Features:** tools only

Summarizes mentions and decisions.

## What you ask

> What did I miss on Slack yesterday?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["slack_mentions"]:::tool
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
| `slack_mentions`: Mentions and threads. | read-only | - |

## Run it

```bash
python usecases/153_slack_catchup/usecase.py                 # your preferred framework
python usecases/153_slack_catchup/usecase.py --all           # all four frameworks
python usecases/153_slack_catchup/usecase.py --manual        # answer the approvals yourself
python usecases/153_slack_catchup/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
