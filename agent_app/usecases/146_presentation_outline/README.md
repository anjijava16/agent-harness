# 146. Outline a presentation

**Area:** Work and career  
**Features:** memory

Pulls the numbers and saves an outline.

## What you ask

> Outline a 10-minute talk on our Q4 results.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["q4_numbers"]:::tool
    RT --> S1
    S2["remember talk_q4"]:::mem
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
| `q4_numbers`: Q4 figures. | read-only | - |

## Run it

```bash
python usecases/146_presentation_outline/usecase.py                 # your preferred framework
python usecases/146_presentation_outline/usecase.py --all           # all four frameworks
python usecases/146_presentation_outline/usecase.py --manual        # answer the approvals yourself
python usecases/146_presentation_outline/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
