# 095. Nightly secrets scan across repos

**When:** 23:40 (night)  
**Trigger:** `cron: 40 23 * * *`  
**Type:** security  
**Deep Agents features:** parallel calls

Opening a security ticket is allowed; the raw secret value never leaves the scan tool.

## What you ask

> Scan all team repos for committed secrets.

## Flow

```mermaid
flowchart TD
    T(["cron: 40 23 * * *"]) --> A["Deep Agent"]
    S1["scan_secrets"]:::tool
    S2["scan_secrets"]:::tool
    A --> S1
    A --> S2
    S3["create_ticket"]:::tool
    S1 --> S3
    S2 --> S3
    Z(["answer to you"])
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
| `scan_secrets` | Scan a repo for secrets. | read-only | - |
| `create_ticket` | Create a ticket. | changes state | - |

## Run it

```bash
python usecases/swe_day/095_secrets_scan_repos/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/095_secrets_scan_repos/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `40 23 * * *` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
