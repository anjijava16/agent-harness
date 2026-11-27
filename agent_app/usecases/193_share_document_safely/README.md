# 193. Share a document safely

**Area:** Documents, accounts and digital life  
**Features:** approval, guard

Creates a link that expires. Public links that never expire are blocked.

## What you ask

> Share my lease with the new landlord.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["share_link - approval, guard"]:::appr
    RT --> S1
    S2["share_link - approval, guard"]:::appr
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
| `share_link`: Create a share link. | talks to someone else | approval, guard |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `share_link`: approve

## Guards

Checked in the shared tool layer before the tool runs, the same on every framework. Guards get your preferences, so changing a limit in the UI changes what's allowed.

- `share_link`

## Run it

```bash
python usecases/193_share_document_safely/usecase.py                 # your preferred framework
python usecases/193_share_document_safely/usecase.py --all           # all four frameworks
python usecases/193_share_document_safely/usecase.py --manual        # answer the approvals yourself
python usecases/193_share_document_safely/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
