# 090. Weekly SLO report

**When:** 22:45 (night)  
**Trigger:** `cron: 45 22 * * 5`  
**Type:** reporting  
**Deep Agents features:** filesystem, parallel calls

Pulls all SLOs in parallel and writes a report people actually skim.

## What you ask

> Write the weekly SLO report.

## Flow

```mermaid
flowchart TD
    T(["cron: 45 22 * * 5"]) --> A["Deep Agent"]
    S1["slo"]:::tool
    S2["slo"]:::tool
    S3["slo"]:::tool
    A --> S1
    A --> S2
    A --> S3
    S4["write /reports/slo-weekly.md"]:::file
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
| `slo` | SLO attainment for a service this week. | read-only | - |

## Run it

```bash
python usecases/swe_day/090_weekly_slo_report/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/090_weekly_slo_report/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `45 22 * * 5` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
