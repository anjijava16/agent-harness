# 192. Close an old account

**Area:** Documents, accounts and digital life  
**Features:** approval

Deleting an account can't be undone, so it needs approval.

## What you ask

> Delete my OldForum account.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["account_status"]:::tool
    RT --> S1
    S2["delete_account - approval"]:::appr
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
| `account_status`: Account status. | read-only | - |
| `delete_account`: Request account deletion. | talks to someone else | approval |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `delete_account`: approve

## Run it

```bash
python usecases/192_cancel_unused_account/usecase.py                 # your preferred framework
python usecases/192_cancel_unused_account/usecase.py --all           # all four frameworks
python usecases/192_cancel_unused_account/usecase.py --manual        # answer the approvals yourself
python usecases/192_cancel_unused_account/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
