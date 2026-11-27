# 068. Release readiness checklist

**When:** 16:10 (release)  
**Trigger:** `manual`  
**Type:** release gate  
**Deep Agents features:** todos, parallel calls

Checks CI, migrations, open blockers and on-call coverage in parallel, tracked as todos.

## What you ask

> Is v2.32.0 ready to ship?

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["plan: 4 todos"]:::plan
    A --> S1
    S2["ci_status"]:::tool
    S3["open_blockers"]:::tool
    S4["pending_migrations"]:::tool
    S5["oncall_now"]:::tool
    S1 --> S2
    S1 --> S3
    S1 --> S4
    S1 --> S5
    Z(["answer to you"])
    S2 --> Z
    S3 --> Z
    S4 --> Z
    S5 --> Z
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
| `ci_status` | CI status for a ref. | read-only | - |
| `open_blockers` | Open release blockers. | read-only | - |
| `pending_migrations` | Migrations in the release. | read-only | - |
| `oncall_now` | Who is on call. | read-only | - |

## Run it

```bash
python usecases/swe_day/068_release_readiness_checklist/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/068_release_readiness_checklist/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
