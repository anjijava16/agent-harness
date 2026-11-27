# 027. Generate a SQL migration with rollback

**When:** 11:00 (coding)  
**Trigger:** `manual`  
**Type:** migration  
**Deep Agents features:** filesystem

Every migration gets a matching down migration; applying to prod is not a tool it has.

## What you ask

> Write the migration for the idempotency_keys table.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["latest_migration"]:::tool
    A --> S1
    S2["write /repo/migrations/0043_idempotency_key..."]:::file
    S1 --> S2
    S3["write /repo/migrations/0043_idempotency_key..."]:::file
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
| `latest_migration` | Latest migration id. | read-only | - |

## Run it

```bash
python usecases/swe_day/027_sql_migration_with_rollback/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/027_sql_migration_with_rollback/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
