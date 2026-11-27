# 049. Tax documents checklist

**Area:** Bills, budget and money admin  
**Features:** parallel calls, memory

Compares what has arrived with last year's list from memory.

## What you ask

> Which tax documents do I still need?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["recall tax"]:::mem
    S2["tax_docs_received"]:::tool
    RT --> S1
    RT --> S2
    Z(["Answer"])
    S1 --> Z
    S2 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef mem fill:#efe,stroke:#8a8
    classDef appr fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
```

## Tools

| Tool | Effect | Control |
|---|---|---|
| `tax_docs_received`: Tax documents received so far. | read-only | - |

## Run it

```bash
python usecases/049_tax_documents_checklist/usecase.py                 # your preferred framework
python usecases/049_tax_documents_checklist/usecase.py --all           # all four frameworks
python usecases/049_tax_documents_checklist/usecase.py --manual        # answer the approvals yourself
python usecases/049_tax_documents_checklist/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
