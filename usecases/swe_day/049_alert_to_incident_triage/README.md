# 049. Alert to incident triage

**When:** 13:30 (ops)  
**Trigger:** `webhook: alertmanager`  
**Type:** incident response  
**Deep Agents features:** filesystem, parallel calls

Pulls metrics, logs and recent deploys in parallel; the triage note is written before a human joins.

## What you ask

> High 5xx on checkout. Triage.

## Flow

```mermaid
flowchart TD
    T(["webhook: alertmanager"]) --> A["Deep Agent"]
    S1["error_rate"]:::tool
    S2["recent_deploys"]:::tool
    S3["top_errors"]:::tool
    A --> S1
    A --> S2
    A --> S3
    S4["write /incidents/checkout-5xx.md"]:::file
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
| `error_rate` | 5xx rate for a service. | read-only | - |
| `recent_deploys` | Deploys in the last N hours. | read-only | - |
| `top_errors` | Most common error lines. | read-only | - |

## Run it

```bash
python usecases/swe_day/049_alert_to_incident_triage/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/049_alert_to_incident_triage/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `alertmanager` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
