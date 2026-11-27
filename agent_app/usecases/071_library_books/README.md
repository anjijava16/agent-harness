# 071. Library books due

**Area:** Shopping, groceries and errands  
**Features:** tools only

Checks the loans and renews the ones it can.

## What you ask

> Any library books due?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["loans"]:::tool
    RT --> S1
    S2["renew"]:::tool
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
| `loans`: Library loans. | read-only | - |
| `renew`: Renew a loan. | changes your data | - |

## Run it

```bash
python usecases/071_library_books/usecase.py                 # your preferred framework
python usecases/071_library_books/usecase.py --all           # all four frameworks
python usecases/071_library_books/usecase.py --manual        # answer the approvals yourself
python usecases/071_library_books/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
