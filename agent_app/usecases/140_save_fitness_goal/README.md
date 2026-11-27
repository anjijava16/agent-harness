# 140. Set a fitness goal

**Area:** Fitness, food and appointments  
**Features:** memory

Saved so workout planning works towards it.

## What you ask

> My goal: run a 10K under 55 minutes by April.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["remember workout"]:::mem
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
| (only `remember` / `recall`) | memory | - |

## Run it

```bash
python usecases/140_save_fitness_goal/usecase.py                 # your preferred framework
python usecases/140_save_fitness_goal/usecase.py --all           # all four frameworks
python usecases/140_save_fitness_goal/usecase.py --manual        # answer the approvals yourself
python usecases/140_save_fitness_goal/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
