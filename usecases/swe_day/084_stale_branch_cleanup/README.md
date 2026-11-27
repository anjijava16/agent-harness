# 084. Stale branch cleanup

**When:** 20:30 (night)  
**Trigger:** `cron: 30 20 * * 0`  
**Type:** repo hygiene  
**Deep Agents features:** guardrail, parallel calls

Runs weekly. Protected branches are blocked by policy no matter what the model decides.

## What you ask

> Delete merged branches older than 30 days.

## Flow

```mermaid
flowchart TD
    T(["cron: 30 20 * * 0"]) --> A["Deep Agent"]
    S1["stale_branches"]:::tool
    A --> S1
    S2["delete_branch (policy guard)"]:::guard
    S3["delete_branch (policy guard)"]:::guard
    S4["delete_branch (policy guard)"]:::guard
    S1 --> S2
    S1 --> S3
    S1 --> S4
    Z(["answer to you"])
    S2 --> Z
    S3 --> Z
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
| `stale_branches` | Merged branches older than N days. | read-only | - |
| `delete_branch` | Delete a remote branch. | changes state | policy guard |

## Run it

```bash
python usecases/swe_day/084_stale_branch_cleanup/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/084_stale_branch_cleanup/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `30 20 * * 0` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Keep the guard. It's ordinary Python in middleware, so it holds even when the model gets it wrong.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
