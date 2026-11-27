# 199. Emergency contact sheet

**Area:** Documents, accounts and digital life  
**Features:** parallel calls, memory, uses preferences

Builds it from contacts and memory, and saves it to the shared family folder.

## What you ask

> Make an emergency contact sheet for the babysitter.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["contacts"]:::tool
    S2["recall plumber"]:::mem
    RT --> S1
    RT --> S2
    S3["file_doc"]:::tool
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
| `contacts`: Contacts by tag. | read-only | - |
| `file_doc`: Save to a folder. | changes your data | - |

## Preferences it uses

| Preference | Default |
|---|---|
| `partner` | Jordan |

## Run it

```bash
python usecases/199_emergency_contacts/usecase.py                 # your preferred framework
python usecases/199_emergency_contacts/usecase.py --all           # all four frameworks
python usecases/199_emergency_contacts/usecase.py --manual        # answer the approvals yourself
python usecases/199_emergency_contacts/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
