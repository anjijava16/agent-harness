# 075. End-of-day Slack update

**When:** 17:30 (release)  
**Trigger:** `cron: 30 17 * * 1-5`  
**Type:** status update  
**Deep Agents features:** HITL

Built from what actually happened today. You edit the message before it posts.

## What you ask

> Post my end-of-day update to #payments-team.

## Flow

```mermaid
flowchart TD
    T(["cron: 30 17 * * 1-5"]) --> A["Deep Agent"]
    S1["my_activity_today"]:::tool
    A --> S1
    S2["slack_post (needs approval)"]:::hitl
    S1 --> S2
    Z(["answer to you"])
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
| `my_activity_today` | PRs, deploys, tickets you touched today. | read-only | - |
| `slack_post` | Post to a Slack channel. | sends something outside | human approval |

## Human decisions in the offline run

- `slack_post`: edited before running (text)

## Run it

```bash
python usecases/swe_day/075_eod_slack_update/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/075_eod_slack_update/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Schedule it with `30 17 * * 1-5` (cron, server time; prefix `CRON_TZ=...` for your zone). A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.
- Approvals: the run pauses on an interrupt. In production, send the pending action to Slack or a web UI and resume with `Command(resume={'decisions': [...]})` on the same `thread_id`. You need a persistent checkpointer (Postgres) for this.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
