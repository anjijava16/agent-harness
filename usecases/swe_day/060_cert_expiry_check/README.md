# 060. TLS certificate expiry check

**When:** 15:15 (ops)  
**Trigger:** `cron: 0 15 * * 1`  
**Type:** monitoring  
**Deep Agents features:** 

Weekly; boring until the week it saves an outage.

## What you ask

> Any certs expiring in the next 30 days?

## Flow

```mermaid
flowchart TD
    T(["cron: 0 15 * * 1"]) --> A["Deep Agent"]
    S1["cert_inventory"]:::tool
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
| `cert_inventory` | All certs and days to expiry. | read-only | - |

## Run it

```bash
python usecases/swe_day/060_cert_expiry_check/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/060_cert_expiry_check/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `0 15 * * 1` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
