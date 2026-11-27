# 006. Standup notes from yesterday's activity

**When:** 07:20 (morning)  
**Trigger:** `cron: 20 7 * * 1-5`  
**Type:** auto-draft  
**Deep Agents features:** AGENTS.md, parallel calls

Builds yesterday/today/blockers from commits and tickets, in the team's format from AGENTS.md.

## What you ask

> Draft my standup update.

## Flow

```mermaid
flowchart TD
    T(["cron: 20 7 * * 1-5"]) --> A["Deep Agent"]
    S1["my_commits"]:::tool
    S2["my_tickets"]:::tool
    A --> S1
    A --> S2
    Z(["answer to you"])
    S1 --> Z
    S2 --> Z
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
| `my_commits` | My commits since a time. | read-only | - |
| `my_tickets` | My tickets by status. | read-only | - |

## House rules (AGENTS.md)

```markdown
# Standup format
Yesterday: ...
Today: ...
Blockers: ...
Max 3 lines each.
```

## Run it

```bash
python usecases/swe_day/006_standup_notes_from_activity/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/006_standup_notes_from_activity/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `20 7 * * 1-5` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
