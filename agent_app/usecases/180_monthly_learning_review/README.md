# 180. Monthly learning review

**Area:** Learning and hobbies  
**Features:** parallel calls, memory

Course, language and practice data in one review.

## What you ask

> What did I learn this month?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["course_progress"]:::tool
    S2["practice_month"]:::tool
    S3["recall spanish"]:::mem
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
| `course_progress`: Course progress. | read-only | - |
| `practice_month`: Practice minutes this month. | read-only | - |

## Run it

```bash
python usecases/180_monthly_learning_review/usecase.py                 # your preferred framework
python usecases/180_monthly_learning_review/usecase.py --all           # all four frameworks
python usecases/180_monthly_learning_review/usecase.py --manual        # answer the approvals yourself
python usecases/180_monthly_learning_review/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
