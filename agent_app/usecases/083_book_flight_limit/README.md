# 083. Book the flight

**Area:** Travel and getting around  
**Features:** approval, guard

Bookings over your review limit are blocked. This one is $248, so it's stopped.

## What you ask

> Book the United flight to Denver.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["book_flight - approval, guard"]:::appr
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
| `book_flight`: Book a flight. | spends money | approval, guard |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `book_flight`: approve

## Guards

Checked in the shared tool layer before the tool runs, the same on every framework. Guards get your preferences, so changing a limit in the UI changes what's allowed.

- `book_flight`

## Run it

```bash
python usecases/083_book_flight_limit/usecase.py                 # your preferred framework
python usecases/083_book_flight_limit/usecase.py --all           # all four frameworks
python usecases/083_book_flight_limit/usecase.py --manual        # answer the approvals yourself
python usecases/083_book_flight_limit/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
