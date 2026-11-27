# 012. Breakfast from what's in the fridge

**Area:** Mornings and daily planning  
**Features:** uses preferences

Uses the fridge inventory and your diet preference.

## What you ask

> What can I make for breakfast?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["fridge_inventory"]:::tool
    RT --> S1
    S2["recipe_search"]:::tool
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
| `fridge_inventory`: What's in the fridge. | read-only | - |
| `recipe_search`: Recipes from ingredients. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `diet` | vegetarian |

## Run it

```bash
python usecases/012_breakfast_idea/usecase.py                 # your preferred framework
python usecases/012_breakfast_idea/usecase.py --all           # all four frameworks
python usecases/012_breakfast_idea/usecase.py --manual        # answer the approvals yourself
python usecases/012_breakfast_idea/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
