# 066. One-off data fix script

**When:** 15:55 (ops)  
**Trigger:** `manual: from ticket`  
**Type:** data fix  
**Deep Agents features:** HITL, filesystem

Writes the script with a dry run first. The real run changes prod data, so it needs approval.

## What you ask

> Fix the 37 invoices stuck in 'pending' after yesterday's outage.

## Flow

```mermaid
flowchart TD
    T(["manual: from ticket"]) --> A["Deep Agent"]
    S1["write /scripts/fix_pending_invoices.sql"]:::file
    A --> S1
    S2["run_sql (needs approval)"]:::hitl
    S1 --> S2
    S3["run_sql (needs approval)"]:::hitl
    S2 --> S3
    Z(["answer to you"])
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
| `run_sql` | Run SQL against prod. | changes state | human approval |

## Human decisions in the offline run

- `run_sql`: call 1: approved; call 2: approved

## Run it

```bash
python usecases/swe_day/066_data_fix_script/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/066_data_fix_script/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Approvals: the run pauses on an interrupt. In production, send the pending action to Slack or a web UI and resume with `Command(resume={'decisions': [...]})` on the same `thread_id`. You need a persistent checkpointer (Postgres) for this.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
