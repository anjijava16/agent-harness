# 177. Word of the day

**Area:** Learning and hobbies  
**Features:** memory

A small daily habit; known words are kept in memory to avoid repeats.

## What you ask

> Teach me a useful word today.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall words_seen"]:::mem
    RT --> S1
    S2["word"]:::tool
    S1 --> S2
    S3["remember words_seen"]:::mem
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
| `word`: A word you haven't seen. | read-only | - |

## Run it

```bash
python usecases/177_word_of_the_day/usecase.py                 # your preferred framework
python usecases/177_word_of_the_day/usecase.py --all           # all four frameworks
python usecases/177_word_of_the_day/usecase.py --manual        # answer the approvals yourself
python usecases/177_word_of_the_day/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
