# 094. API usage analytics

**When:** 23:30 (night)  
**Trigger:** `cron: 30 23 * * 0`  
**Type:** analytics  
**Deep Agents features:** structured output

Tells you which clients to chase before turning v1 off.

## What you ask

> Who still calls the deprecated v1 endpoints?

## Flow

```mermaid
flowchart TD
    T(["cron: 30 23 * * 0"]) --> A["Deep Agent"]
    S1["endpoint_usage"]:::tool
    A --> S1
    S2["structured answer: V1Usage"]:::out
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
| `endpoint_usage` | Calls per client for an endpoint prefix. | read-only | - |

## Run it

```bash
python usecases/swe_day/094_api_usage_analytics/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/094_api_usage_analytics/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `30 23 * * 0` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- The `V1Usage` result is a Pydantic object, so you can post it straight to a dashboard or database.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
