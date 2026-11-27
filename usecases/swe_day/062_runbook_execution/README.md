# 062. Follow a runbook step by step

**When:** 15:35 (ops)  
**Trigger:** `manual`  
**Type:** runbook  
**Deep Agents features:** HITL, todos, filesystem

Reads the runbook and runs it as a todo list; the cordon/drain steps need approval.

## What you ask

> Run the 'drain a node' runbook for node ip-10-0-3-7.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["read /runbooks/drain-node.md"]:::file
    A --> S1
    S2["plan: 3 todos"]:::plan
    S1 --> S2
    S3["kubectl (needs approval)"]:::hitl
    S2 --> S3
    S4["kubectl (needs approval)"]:::hitl
    S3 --> S4
    Z(["answer to you"])
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
| `kubectl` | Run a kubectl command. | changes state | human approval |

## Human decisions in the offline run

- `kubectl`: approved

## Run it

```bash
python usecases/swe_day/062_runbook_execution/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/062_runbook_execution/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Approvals: the run pauses on an interrupt. In production, send the pending action to Slack or a web UI and resume with `Command(resume={'decisions': [...]})` on the same `thread_id`. You need a persistent checkpointer (Postgres) for this.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
