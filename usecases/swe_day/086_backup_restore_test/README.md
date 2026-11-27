# 086. Backup restore test

**When:** 21:30 (night)  
**Trigger:** `cron: 30 21 * * 6`  
**Type:** DR  
**Deep Agents features:** guardrail

A backup you haven't restored is a guess. The restore target is checked so it never points at prod.

## What you ask

> Restore last night's ledger backup to a scratch DB and verify it.

## Flow

```mermaid
flowchart TD
    T(["cron: 30 21 * * 6"]) --> A["Deep Agent"]
    S1["restore_backup (policy guard)"]:::guard
    A --> S1
    S2["restore_backup (policy guard)"]:::guard
    S1 --> S2
    S3["row_counts"]:::tool
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
| `restore_backup` | Restore a backup to a target DB. | changes state | policy guard |
| `row_counts` | Row counts in a DB. | read-only | - |

## Run it

```bash
python usecases/swe_day/086_backup_restore_test/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/086_backup_restore_test/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `30 21 * * 6` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Keep the guard. It's ordinary Python in middleware, so it holds even when the model gets it wrong.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
