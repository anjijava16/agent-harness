# 066. Book a haircut

**Area:** Shopping, groceries and errands  
**Features:** approval, memory

Remembers your barber and preferred time, finds a slot, books after approval.

## What you ask

> Book my usual haircut next week.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall haircut"]:::mem
    RT --> S1
    S2["salon_slots"]:::tool
    S1 --> S2
    S3["book - approval"]:::appr
    S2 --> S3
    Z(["Answer"])
    S3 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `salon_slots`: Open slots. | read-only | - |
| `book`: Book a slot. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `book`: approve

## Run it

```bash
python usecases/066_book_haircut/usecase.py                 # your preferred framework
python usecases/066_book_haircut/usecase.py --all           # all four frameworks
python usecases/066_book_haircut/usecase.py --manual        # answer the approvals yourself
python usecases/066_book_haircut/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
