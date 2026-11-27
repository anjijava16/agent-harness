# 051. Set up rent autopay

**Area:** Bills, budget and money admin  
**Features:** approval, guard

Creating recurring payments needs approval. Amounts over $3,000 are blocked.

## What you ask

> Set up rent autopay for the 1st.

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["create_autopay - approval, guard"]:::appr
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
| `create_autopay`: Create a recurring payment. | spends money | approval, guard |

## Approvals

In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:

- `create_autopay`: approve

## Guards

Checked in the shared tool layer before the tool runs, the same on every framework. Guards get your preferences, so changing a limit in the UI changes what's allowed.

- `create_autopay`

## Run it

```bash
python usecases/051_rent_reminder_autopay/usecase.py                 # your preferred framework
python usecases/051_rent_reminder_autopay/usecase.py --all           # all four frameworks
python usecases/051_rent_reminder_autopay/usecase.py --manual        # answer the approvals yourself
python usecases/051_rent_reminder_autopay/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
