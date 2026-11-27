# 089. Quarantine flaky tests

**When:** 22:30 (night)  
**Trigger:** `cron: 30 22 * * *`  
**Type:** CI hygiene  
**Deep Agents features:** filesystem

Edits the quarantine list file and opens a PR. People decide whether to fix or delete.

## What you ask

> Quarantine tests that flaked more than 3 times this week.

## Flow

```mermaid
flowchart TD
    T(["cron: 30 22 * * *"]) --> A["Deep Agent"]
    S1["flake_counts"]:::tool
    A --> S1
    S2["read /repo/tests/quarantine.txt"]:::file
    S1 --> S2
    S3["edit /repo/tests/quarantine.txt"]:::file
    S2 --> S3
    S4["open_pr"]:::tool
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
| `flake_counts` | Flake counts this week. | read-only | - |
| `open_pr` | Open a PR. | sends something outside | - |

## Run it

```bash
python usecases/swe_day/089_flaky_test_quarantine/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/089_flaky_test_quarantine/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `30 22 * * *` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
