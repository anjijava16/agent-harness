# 003. PR review queue prioritizer

**When:** 06:50 (morning)  
**Trigger:** `cron: 50 6 * * 1-5`  
**Type:** scheduled triage  
**Deep Agents features:** structured output

Ranks review requests by blocking impact and age; output is typed so a Slack bot can post it.

## What you ask

> Which PRs should I review first today?

## Flow

```mermaid
flowchart TD
    T(["cron: 50 6 * * 1-5"]) --> A["Deep Agent"]
    S1["review_requests"]:::tool
    A --> S1
    S2["structured answer: ReviewQueue"]:::out
    S1 --> S2
    Z(["typed result"])
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
| `review_requests` | PRs where I'm a requested reviewer. | read-only | - |

## Run it

```bash
python usecases/swe_day/003_pr_review_queue_prioritizer/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/003_pr_review_queue_prioritizer/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `50 6 * * 1-5` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- The `ReviewQueue` result is a Pydantic object, so you can post it straight to a dashboard or database.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
