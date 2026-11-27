# 092. Benchmark regression check

**When:** 23:10 (night)  
**Trigger:** `cron: 10 23 * * *`  
**Type:** performance  
**Deep Agents features:** 

Compares tonight's benchmark run with the 7-day median.

## What you ask

> Did any benchmark regress more than 10% today?

## Flow

```mermaid
flowchart TD
    T(["cron: 10 23 * * *"]) --> A["Deep Agent"]
    S1["bench_results"]:::tool
    A --> S1
    Z(["answer to you"])
    S1 --> Z
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
| `bench_results` | Benchmark results vs 7-day median. | read-only | - |

## Run it

```bash
python usecases/swe_day/092_benchmark_regression_check/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/092_benchmark_regression_check/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `10 23 * * *` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
