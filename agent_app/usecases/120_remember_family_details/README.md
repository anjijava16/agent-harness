# 120. Remember family details

**Area:** Home, family and pets  
**Features:** memory

Saves it so meal planning uses it.

## What you ask

> Remember: Maya likes cheese and pasta, hates mushrooms.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["remember family_likes"]:::mem
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
| (only `remember` / `recall`) | memory | - |

## Run it

```bash
python usecases/120_remember_family_details/usecase.py                 # your preferred framework
python usecases/120_remember_family_details/usecase.py --all           # all four frameworks
python usecases/120_remember_family_details/usecase.py --manual        # answer the approvals yourself
python usecases/120_remember_family_details/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
