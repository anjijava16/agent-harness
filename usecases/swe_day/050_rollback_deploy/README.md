# 050. Roll back a bad deploy

**When:** 13:40 (ops)  
**Trigger:** `manual: from incident`  
**Type:** deploy  
**Deep Agents features:** HITL

A rollback touches prod, so it waits for your approval.

## What you ask

> Roll checkout back to v2.30.4.

## Flow

```mermaid
flowchart TD
    T(["manual: from incident"]) --> A["Deep Agent"]
    S1["rollback (needs approval)"]:::hitl
    A --> S1
    S2["error_rate"]:::tool
    S1 --> S2
    Z(["answer to you"])
    S2 --> Z
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
| `rollback` | Roll a service back to a version. | changes state | human approval |
| `error_rate` | 5xx rate. | read-only | - |

## Human decisions in the offline run

- `rollback`: approved

## Run it

```bash
python usecases/swe_day/050_rollback_deploy/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/050_rollback_deploy/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Approvals: the run pauses on an interrupt. In production, send the pending action to Slack or a web UI and resume with `Command(resume={'decisions': [...]})` on the same `thread_id`. You need a persistent checkpointer (Postgres) for this.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
