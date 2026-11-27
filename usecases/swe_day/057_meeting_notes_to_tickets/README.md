# 057. Meeting notes to tickets

**When:** 14:45 (ops)  
**Trigger:** `webhook: meeting_transcript_ready`  
**Type:** ticket creation  
**Deep Agents features:** HITL, parallel calls

Pulls the action items out and creates tickets; one isn't a real task and gets rejected.

## What you ask

> Turn the architecture sync transcript into tickets.

## Flow

```mermaid
flowchart TD
    T(["webhook: meeting_transcript_ready"]) --> A["Deep Agent"]
    S1["get_transcript"]:::tool
    A --> S1
    S2["create_ticket (needs approval)"]:::hitl
    S3["create_ticket (needs approval)"]:::hitl
    S4["create_ticket (needs approval)"]:::hitl
    S1 --> S2
    S1 --> S3
    S1 --> S4
    Z(["answer to you"])
    S2 --> Z
    S3 --> Z
    S4 --> Z
    classDef tool fill:#eef,stroke:#88a
    classDef file fill:#efe,stroke:#8a8
    classDef sub fill:#fef3dd,stroke:#c90
    classDef plan fill:#f4f4f4,stroke:#999
    classDef hitl fill:#fde,stroke:#c48
    classDef guard fill:#fee,stroke:#c44
    classDef out fill:#e8f6ff,stroke:#48c
```

## Tools

| Tool | What it does | Effect | Control |
|---|---|---|---|
| `get_transcript` | Meeting transcript. | read-only | - |
| `create_ticket` | Create a ticket. | changes state | human approval |

## Human decisions in the offline run

- `create_ticket`: call 1: approved; call 2: approved; call 3: rejected

## Run it

```bash
python usecases/swe_day/057_meeting_notes_to_tickets/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/057_meeting_notes_to_tickets/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `meeting_transcript_ready` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- Approvals: the run pauses on an interrupt. In production, send the pending action to Slack or a web UI and resume with `Command(resume={'decisions': [...]})` on the same `thread_id`. You need a persistent checkpointer (Postgres) for this.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
