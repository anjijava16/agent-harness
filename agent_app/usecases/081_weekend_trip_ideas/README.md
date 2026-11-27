# 081. Weekend trip ideas

**Area:** Travel and getting around  
**Features:** parallel calls, uses preferences

Checks drive times and weekend weather for a few places in parallel.

## What you ask

> Ideas for a weekend away within 4 hours' drive?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["drive_time_to"]:::tool
    S2["drive_time_to"]:::tool
    S3["drive_time_to"]:::tool
    RT --> S1
    RT --> S2
    RT --> S3
    S4["weekend_weather"]:::tool
    S5["weekend_weather"]:::tool
    S1 --> S4
    S1 --> S5
    S2 --> S4
    S2 --> S5
    S3 --> S4
    S3 --> S5
    Z(["Answer"])
    S4 --> Z
    S5 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `drive_time_to`: Drive time from your city. | read-only | - |
| `weekend_weather`: Weekend forecast. | read-only | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `home_city` | Chicago |

## Run it

```bash
python usecases/081_weekend_trip_ideas/usecase.py                 # your preferred framework
python usecases/081_weekend_trip_ideas/usecase.py --all           # all four frameworks
python usecases/081_weekend_trip_ideas/usecase.py --manual        # answer the approvals yourself
python usecases/081_weekend_trip_ideas/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
