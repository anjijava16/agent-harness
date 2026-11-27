# 020. Break an epic into tickets

**When:** 09:40 (planning)  
**Trigger:** `manual`  
**Type:** ticket creation  
**Deep Agents features:** HITL, parallel calls

Creating tickets is a write; the batch is approved, and one ticket is edited before creation.

## What you ask

> Split the 'Invoice exports' epic into tickets.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["create_ticket (needs approval)"]:::hitl
    S2["create_ticket (needs approval)"]:::hitl
    S3["create_ticket (needs approval)"]:::hitl
    A --> S1
    A --> S2
    A --> S3
    Z(["answer to you"])
    S1 --> Z
    S2 --> Z
    S3 --> Z
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
| `create_ticket` | Create a Jira ticket. | changes state | human approval |

## Human decisions in the offline run

- `create_ticket`: call 1: approved; call 2: edited before running (title); call 3: approved

## Run it

```bash
python usecases/swe_day/020_epic_to_tickets/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/020_epic_to_tickets/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Approvals: the run pauses on an interrupt. In production, send the pending action to Slack or a web UI and resume with `Command(resume={'decisions': [...]})` on the same `thread_id`. You need a persistent checkpointer (Postgres) for this.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
