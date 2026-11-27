# 011. Focus mode until noon

**Area:** Mornings and daily planning  
**Features:** parallel calls, approval

Sets your Slack status and do-not-disturb, then moves one meeting after you approve.

## What you ask

> Turn on focus mode until noon.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["set_status"]:::tool
    S2["dnd"]:::tool
    RT --> S1
    RT --> S2
    S3["move_meeting - approval"]:::appr
    S1 --> S3
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
| `set_status`: Set chat status. | changes your data | - |
| `dnd`: Do not disturb until a time. | changes your data | - |
| `move_meeting`: Move a meeting. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `move_meeting`: approve

## Run it

```bash
python usecases/011_focus_mode/usecase.py                 # your preferred framework
python usecases/011_focus_mode/usecase.py --all           # all four frameworks
python usecases/011_focus_mode/usecase.py --manual        # answer the approvals yourself
python usecases/011_focus_mode/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
