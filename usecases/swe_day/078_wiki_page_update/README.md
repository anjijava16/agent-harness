# 078. Update the team wiki

**When:** 18:00 (release)  
**Trigger:** `manual`  
**Type:** docs  
**Deep Agents features:** HITL

Small doc updates are easy to skip. This makes them a 30-second task.

## What you ask

> Add today's incident learnings to the checkout runbook page.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["wiki_get"]:::tool
    A --> S1
    S2["wiki_update (needs approval)"]:::hitl
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
| `wiki_get` | Get a wiki page. | read-only | - |
| `wiki_update` | Update a wiki page. | sends something outside | human approval |

## Human decisions in the offline run

- `wiki_update`: approved

## Run it

```bash
python usecases/swe_day/078_wiki_page_update/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/078_wiki_page_update/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Approvals: the run pauses on an interrupt. In production, send the pending action to Slack or a web UI and resume with `Command(resume={'decisions': [...]})` on the same `thread_id`. You need a persistent checkpointer (Postgres) for this.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
