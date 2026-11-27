# 041. Resolve a merge conflict

**When:** 12:50 (review)  
**Trigger:** `manual`  
**Type:** git  
**Deep Agents features:** filesystem

Reads both sides of the conflict, keeps both intents, reruns tests.

## What you ask

> Rebase my branch on main; there's a conflict in fees.py.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["read /repo/payments/fees.py"]:::file
    A --> S1
    S2["write /repo/payments/fees.py"]:::file
    S1 --> S2
    S3["run_tests"]:::tool
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
| `run_tests` | Run tests. | read-only | - |

## Run it

```bash
python usecases/swe_day/041_resolve_merge_conflict/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/041_resolve_merge_conflict/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
