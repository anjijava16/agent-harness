# 122. Book a gym class

**Area:** Fitness, food and appointments  
**Features:** approval

Finds a class and books after approval.

## What you ask

> Book a spin class for Wednesday evening.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["classes"]:::tool
    RT --> S1
    S2["book_class - approval"]:::appr
    S1 --> S2
    Z(["Answer"])
    S2 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `classes`: Gym classes. | read-only | - |
| `book_class`: Book a class. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `book_class`: approve

## Run it

```bash
python usecases/122_book_gym_class/usecase.py                 # your preferred framework
python usecases/122_book_gym_class/usecase.py --all           # all four frameworks
python usecases/122_book_gym_class/usecase.py --manual        # answer the approvals yourself
python usecases/122_book_gym_class/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
