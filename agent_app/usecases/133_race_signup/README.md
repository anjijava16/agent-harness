# 133. Sign up for a 10K

**Area:** Fitness, food and appointments  
**Features:** approval

Registration is a payment, so it needs approval.

## What you ask

> Sign me up for the spring 10K.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["race_info"]:::tool
    RT --> S1
    S2["register_race - approval"]:::appr
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
| `race_info`: Race details. | read-only | - |
| `register_race`: Register for a race. | spends money | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `register_race`: approve

## Run it

```bash
python usecases/133_race_signup/usecase.py                 # your preferred framework
python usecases/133_race_signup/usecase.py --all           # all four frameworks
python usecases/133_race_signup/usecase.py --manual        # answer the approvals yourself
python usecases/133_race_signup/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
