# 015. Packages arriving today

**Area:** Mornings and daily planning  
**Features:** parallel calls

Checks every carrier at once.

## What you ask

> Are any packages coming today?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["track"]:::tool
    S2["track"]:::tool
    S3["track"]:::tool
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
| `track`: Track packages with a carrier. | read-only | - |

## Run it

```bash
python usecases/015_package_tracking/usecase.py                 # your preferred framework
python usecases/015_package_tracking/usecase.py --all           # all four frameworks
python usecases/015_package_tracking/usecase.py --manual        # answer the approvals yourself
python usecases/015_package_tracking/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
