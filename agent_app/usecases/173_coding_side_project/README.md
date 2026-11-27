# 173. Side project: what's next

**Area:** Learning and hobbies  
**Features:** parallel calls, memory

Reads the issue list and your notes, then picks one task.

## What you ask

> What's next on my side project?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["open_issues"]:::tool
    S2["recall side_project"]:::mem
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
| `open_issues`: Open issues in a repo. | read-only | - |

## Run it

```bash
python usecases/173_coding_side_project/usecase.py                 # your preferred framework
python usecases/173_coding_side_project/usecase.py --all           # all four frameworks
python usecases/173_coding_side_project/usecase.py --manual        # answer the approvals yourself
python usecases/173_coding_side_project/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
