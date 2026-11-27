# 034. Voicemails to text

**Area:** Email, messages and calendar  
**Features:** tools only

Transcribes them and flags the one that needs a call back.

## What you ask

> What are my voicemails about?

## Flow

```mermaid
flowchart TD
    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]
    S1["voicemails"]:::tool
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
| `voicemails`: Transcribed voicemails. | read-only | - |

## Run it

```bash
python usecases/034_voicemail_transcribe/usecase.py                 # your preferred framework
python usecases/034_voicemail_transcribe/usecase.py --all           # all four frameworks
python usecases/034_voicemail_transcribe/usecase.py --manual        # answer the approvals yourself
python usecases/034_voicemail_transcribe/usecase.py --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)
```

Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.
