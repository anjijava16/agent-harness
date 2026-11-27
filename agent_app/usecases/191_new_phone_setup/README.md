# 191. New phone checklist

**Area:** Documents, accounts and digital life  
**Features:** parallel calls, memory

Builds a checklist from the apps and 2FA you saved in memory.

## What you ask

> I got a new phone. What do I need to move over?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["app_list"]:::tool
    S2["recall 2fa"]:::mem
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
| `app_list`: Apps on the old phone. | read-only | - |

## Run it

```bash
python usecases/191_new_phone_setup/usecase.py                 # your preferred framework
python usecases/191_new_phone_setup/usecase.py --all           # all four frameworks
python usecases/191_new_phone_setup/usecase.py --manual        # answer the approvals yourself
python usecases/191_new_phone_setup/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
