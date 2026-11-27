# 174. Book a cooking class

**Area:** Learning and hobbies  
**Features:** approval, uses preferences

Booking for two, with approval.

## What you ask

> Book a pasta-making class for Jordan and me.

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
| `classes`: Classes. | read-only | - |
| `book_class`: Book a class. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `book_class`: approve

## Preferences it uses

| Preference | Default |
|---|---|
| `partner` | Jordan |

## Run it

```bash
python usecases/174_cooking_class/usecase.py                 # your preferred framework
python usecases/174_cooking_class/usecase.py --all           # all four frameworks
python usecases/174_cooking_class/usecase.py --manual        # answer the approvals yourself
python usecases/174_cooking_class/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
