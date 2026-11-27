# 165. Study schedule

**Area:** Learning and hobbies  
**Features:** parallel calls

Two sessions a week, in free evening slots.

## What you ask

> Put my course study sessions on the calendar.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["free_slots"]:::tool
    RT --> S1
    S2["add_event"]:::tool
    S3["add_event"]:::tool
    S1 --> S2
    S1 --> S3
    Z(["Answer"])
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
| `free_slots`: Free slots. | read-only | - |
| `add_event`: Add a calendar event. | changes your data | - |

## Run it

```bash
python usecases/165_study_schedule/usecase.py                 # your preferred framework
python usecases/165_study_schedule/usecase.py --all           # all four frameworks
python usecases/165_study_schedule/usecase.py --manual        # answer the approvals yourself
python usecases/165_study_schedule/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
