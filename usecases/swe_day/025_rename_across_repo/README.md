# 025. Rename a function across the repo

**When:** 10:30 (coding)  
**Trigger:** `manual`  
**Type:** refactor  
**Deep Agents features:** filesystem

grep-then-edit over real files, then run the tests.

## What you ask

> Rename calc_fee to compute_fee everywhere.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["grep /repo"]:::file
    A --> S1
    S2["edit /repo/payments/fees.py"]:::file
    S1 --> S2
    S3["edit /repo/payments/api.py"]:::file
    S2 --> S3
    S4["run_tests"]:::tool
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
| `run_tests` | Run the test suite. | read-only | - |

## Run it

```bash
python usecases/swe_day/025_rename_across_repo/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/025_rename_across_repo/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
