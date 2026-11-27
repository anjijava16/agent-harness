# 148. Add a win to my resume

**Area:** Work and career  
**Features:** approval

Edits your resume doc after you approve the wording.

## What you ask

> Add the quarterly report project to my resume.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["append_resume - approval"]:::appr
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
| `append_resume`: Append a bullet to the resume. | changes your data | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `append_resume`: approve with edits `bullet='Led the Q4 business review across 4 teams; cut prep time from 3 weeks to 1'`

## Run it

```bash
python usecases/148_update_resume/usecase.py                 # your preferred framework
python usecases/148_update_resume/usecase.py --all           # all four frameworks
python usecases/148_update_resume/usecase.py --manual        # answer the approvals yourself
python usecases/148_update_resume/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
