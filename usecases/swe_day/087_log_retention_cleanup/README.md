# 087. Log retention cleanup

**When:** 22:00 (night)  
**Trigger:** `cron: 0 22 * * 0`  
**Type:** maintenance  
**Deep Agents features:** guardrail, parallel calls

Deletion is allowed only for debug-level indices; audit logs are blocked.

## What you ask

> Delete debug logs older than 14 days.

## Flow

```mermaid
flowchart TD
    T(["cron: 0 22 * * 0"]) --> A["Deep Agent"]
    S1["old_indices"]:::tool
    A --> S1
    S2["delete_index (policy guard)"]:::guard
    S3["delete_index (policy guard)"]:::guard
    S1 --> S2
    S1 --> S3
    Z(["answer to you"])
    S2 --> Z
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
| `old_indices` | Log indices older than N days. | read-only | - |
| `delete_index` | Delete a log index. | changes state | policy guard |

## Run it

```bash
python usecases/swe_day/087_log_retention_cleanup/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/087_log_retention_cleanup/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `0 22 * * 0` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Keep the guard. It's ordinary Python in middleware, so it holds even when the model gets it wrong.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
