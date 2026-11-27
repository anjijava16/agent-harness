# 100. Weekly retro draft

**When:** 23:59 (night)  
**Trigger:** `cron: 59 23 * * 5`  
**Type:** reflection  
**Deep Agents features:** long-term memory, filesystem

Reads the week's learnings from long-term memory and the shipped work, and drafts the retro for Monday.

## What you ask

> Draft my weekly retro.

## Flow

```mermaid
flowchart TD
    T(["cron: 59 23 * * 5"]) --> A["Deep Agent"]
    S1["write /memories/learnings.md"]:::file
    A --> S1
    S2["read /memories/learnings.md"]:::file
    S1 --> S2
    S3["shipped_this_week"]:::tool
    S2 --> S3
    S4["write /retro/week-48.md"]:::file
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
| `shipped_this_week` | Work shipped this week. | read-only | - |

## Run it

```bash
python usecases/swe_day/100_weekly_retro_draft/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/100_weekly_retro_draft/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `59 23 * * 5` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- `/memories/` maps to a LangGraph store. Use `PostgresStore` so the next run (or tomorrow's) can read it.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
