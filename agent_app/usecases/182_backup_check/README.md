# 182. Are my backups working

**Area:** Documents, accounts and digital life  
**Features:** parallel calls

Checks both backup services.

## What you ask

> Did my laptop and phone back up this week?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["last_backup"]:::tool
    S2["last_backup"]:::tool
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
| `last_backup`: Last backup of a device. | read-only | - |

## Run it

```bash
python usecases/182_backup_check/usecase.py                 # your preferred framework
python usecases/182_backup_check/usecase.py --all           # all four frameworks
python usecases/182_backup_check/usecase.py --manual        # answer the approvals yourself
python usecases/182_backup_check/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
