# 098. Watch upstream OSS issues we depend on

**When:** 23:55 (night)  
**Trigger:** `cron: 55 23 * * *`  
**Type:** monitoring  
**Deep Agents features:** parallel calls

Checks issues you starred so you hear when a fix lands.

## What you ask

> Any news on the upstream issues we're tracking?

## Flow

```mermaid
flowchart TD
    T(["cron: 55 23 * * *"]) --> A["Deep Agent"]
    S1["issue_status"]:::tool
    S2["issue_status"]:::tool
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
| `issue_status` | Status of a GitHub issue. | read-only | - |

## Run it

```bash
python usecases/swe_day/098_upstream_issue_watcher/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/098_upstream_issue_watcher/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `55 23 * * *` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
