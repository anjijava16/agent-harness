# 012. SLO and error budget status

**When:** 08:05 (morning)  
**Trigger:** `cron: 5 8 * * 1-5`  
**Type:** scheduled check  
**Deep Agents features:** parallel calls

Simple math done reliably every morning, and a freeze suggestion when budget is low.

## What you ask

> How much error budget do my services have left?

## Flow

```mermaid
flowchart TD
    T(["cron: 5 8 * * 1-5"]) --> A["Deep Agent"]
    S1["slo_status"]:::tool
    S2["slo_status"]:::tool
    A --> S1
    A --> S2
    Z(["answer to you"])
    S1 --> Z
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
| `slo_status` | SLO and remaining error budget. | read-only | - |

## Run it

```bash
python usecases/swe_day/012_slo_error_budget_status/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/012_slo_error_budget_status/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `5 8 * * 1-5` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
