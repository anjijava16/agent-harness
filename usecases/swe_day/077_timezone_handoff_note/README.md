# 077. Handoff note for the other timezone

**When:** 17:50 (release)  
**Trigger:** `cron: 50 17 * * 1-5`  
**Type:** handoff  
**Deep Agents features:** filesystem, parallel calls

So the morning team in another timezone doesn't start by asking what happened.

## What you ask

> Write the handoff for the Bangalore team.

## Flow

```mermaid
flowchart TD
    T(["cron: 50 17 * * 1-5"]) --> A["Deep Agent"]
    S1["open_incidents"]:::tool
    S2["in_flight_deploys"]:::tool
    A --> S1
    A --> S2
    S3["write /handoff/today.md"]:::file
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
| `open_incidents` | Open incidents. | read-only | - |
| `in_flight_deploys` | Deploys in progress. | read-only | - |

## Run it

```bash
python usecases/swe_day/077_timezone_handoff_note/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/077_timezone_handoff_note/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `50 17 * * 1-5` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
