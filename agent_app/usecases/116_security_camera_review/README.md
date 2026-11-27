# 116. Who came to the door

**Area:** Home, family and pets  
**Features:** tools only

Summarizes doorbell events.

## What you ask

> Who came to the door today?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["doorbell_events"]:::tool
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
| `doorbell_events`: Doorbell events. | read-only | - |

## Run it

```bash
python usecases/116_security_camera_review/usecase.py                 # your preferred framework
python usecases/116_security_camera_review/usecase.py --all           # all four frameworks
python usecases/116_security_camera_review/usecase.py --manual        # answer the approvals yourself
python usecases/116_security_camera_review/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
