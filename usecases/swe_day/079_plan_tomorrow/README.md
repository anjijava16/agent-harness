# 079. Plan tomorrow

**When:** 18:10 (release)  
**Trigger:** `cron: 10 18 * * 1-5`  
**Type:** planning  
**Deep Agents features:** long-term memory, todos, filesystem, parallel calls

Keeps a running plan in long-term memory, so tomorrow's morning run picks it up.

## What you ask

> Plan my tomorrow.

## Flow

```mermaid
flowchart TD
    T(["cron: 10 18 * * 1-5"]) --> A["Deep Agent"]
    S1["calendar_tomorrow"]:::tool
    S2["my_open_tickets"]:::tool
    A --> S1
    A --> S2
    S3["plan: 3 todos"]:::plan
    S1 --> S3
    S2 --> S3
    S4["write /memories/tomorrow.md"]:::file
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
| `calendar_tomorrow` | Tomorrow's meetings. | read-only | - |
| `my_open_tickets` | My open tickets. | read-only | - |

## Run it

```bash
python usecases/swe_day/079_plan_tomorrow/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/079_plan_tomorrow/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `10 18 * * 1-5` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- `/memories/` maps to a LangGraph store. Use `PostgresStore` so the next run (or tomorrow's) can read it.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
