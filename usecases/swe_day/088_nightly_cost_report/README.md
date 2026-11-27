# 088. Nightly cost report

**When:** 22:15 (night)  
**Trigger:** `cron: 15 22 * * *`  
**Type:** FinOps  
**Deep Agents features:** structured output

Structured output feeds a dashboard; the agent just does the gathering.

## What you ask

> Summarise today's cloud spend by service.

## Flow

```mermaid
flowchart TD
    T(["cron: 15 22 * * *"]) --> A["Deep Agent"]
    S1["cost_by_service"]:::tool
    A --> S1
    S2["structured answer: CostReport"]:::out
    S1 --> S2
    Z(["typed result"])
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
| `cost_by_service` | Spend by service today. | read-only | - |

## Run it

```bash
python usecases/swe_day/088_nightly_cost_report/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/088_nightly_cost_report/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `15 22 * * *` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- The `CostReport` result is a Pydantic object, so you can post it straight to a dashboard or database.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
