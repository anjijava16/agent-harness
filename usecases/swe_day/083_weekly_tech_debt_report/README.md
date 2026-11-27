# 083. Weekly tech-debt report

**When:** 20:00 (night)  
**Trigger:** `cron: 0 20 * * 5`  
**Type:** reporting  
**Deep Agents features:** filesystem, parallel calls

Counts TODOs, deprecated calls and big files; writes a report the team skims on Monday.

## What you ask

> Build the weekly tech-debt report.

## Flow

```mermaid
flowchart TD
    T(["cron: 0 20 * * 5"]) --> A["Deep Agent"]
    S1["count_todos"]:::tool
    S2["deprecated_usage"]:::tool
    S3["largest_files"]:::tool
    A --> S1
    A --> S2
    A --> S3
    S4["write /reports/tech-debt-weekly.md"]:::file
    S1 --> S4
    S2 --> S4
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
| `count_todos` | TODO/FIXME count by dir. | read-only | - |
| `deprecated_usage` | Deprecated API usages. | read-only | - |
| `largest_files` | Largest source files. | read-only | - |

## Run it

```bash
python usecases/swe_day/083_weekly_tech_debt_report/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/083_weekly_tech_debt_report/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `0 20 * * 5` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
