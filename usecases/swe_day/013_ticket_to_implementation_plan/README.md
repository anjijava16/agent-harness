# 013. Jira ticket to implementation plan

**When:** 08:30 (planning)  
**Trigger:** `manual: ticket assigned`  
**Type:** planning  
**Deep Agents features:** todos, filesystem, parallel calls

Reads the ticket and the code it touches, then lays out the steps as a todo list you can follow.

## What you ask

> Turn PAY-431 into an implementation plan.

## Flow

```mermaid
flowchart TD
    T(["manual: ticket assigned"]) --> A["Deep Agent"]
    S1["get_ticket"]:::tool
    S2["search_code"]:::tool
    A --> S1
    A --> S2
    S3["plan: 5 todos"]:::plan
    S1 --> S3
    S2 --> S3
    S4["write /plans/PAY-431.md"]:::file
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
| `get_ticket` | Fetch a Jira ticket. | read-only | - |
| `search_code` | Search the codebase. | read-only | - |

## Run it

```bash
python usecases/swe_day/013_ticket_to_implementation_plan/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/013_ticket_to_implementation_plan/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
