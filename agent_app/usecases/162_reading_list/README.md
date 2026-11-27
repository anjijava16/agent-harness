# 162. What should I read next

**Area:** Learning and hobbies  
**Features:** parallel calls, memory

Uses books you liked (saved in memory) and checks library availability.

## What you ask

> What should I read next?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall books"]:::mem
    RT --> S1
    S2["book_recs"]:::tool
    S1 --> S2
    S3["library_availability"]:::tool
    S4["library_availability"]:::tool
    S2 --> S3
    S2 --> S4
    Z(["Answer"])
    S3 --> Z
    S4 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `book_recs`: Recommendations from liked books. | read-only | - |
| `library_availability`: Library availability. | read-only | - |

## Run it

```bash
python usecases/162_reading_list/usecase.py                 # your preferred framework
python usecases/162_reading_list/usecase.py --all           # all four frameworks
python usecases/162_reading_list/usecase.py --manual        # answer the approvals yourself
python usecases/162_reading_list/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
