# 005. Meeting prep pack

**When:** 07:10 (morning)  
**Trigger:** `cron: 10 7 * * 1-5`  
**Type:** scheduled prep  
**Deep Agents features:** filesystem

Fetches the docs and open questions for each meeting so you walk in with context.

## What you ask

> Prep me for today's meetings.

## Flow

```mermaid
flowchart TD
    T(["cron: 10 7 * * 1-5"]) --> A["Deep Agent"]
    S1["calendar_today"]:::tool
    A --> S1
    S2["get_doc"]:::tool
    S1 --> S2
    S3["write /prep/today.md"]:::file
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
| `calendar_today` | Today's meetings. | read-only | - |
| `get_doc` | Fetch a doc's open comments. | read-only | - |

## Run it

```bash
python usecases/swe_day/005_meeting_prep_pack/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/005_meeting_prep_pack/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `10 7 * * 1-5` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
