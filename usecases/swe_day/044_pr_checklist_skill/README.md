# 044. PR checklist check

**When:** 13:05 (review)  
**Trigger:** `webhook: pull_request.opened`  
**Type:** policy check  
**Deep Agents features:** skills, filesystem, structured output

The checklist lives in a skill, so changing the rules means editing one file.

## What you ask

> Does PR #820 meet our merge checklist?

## Flow

```mermaid
flowchart TD
    T(["webhook: pull_request.opened"]) --> A["Deep Agent"]
    S1["read /skills/pr-checklist/SKILL.md"]:::file
    A --> S1
    S2["pr_facts"]:::tool
    S1 --> S2
    S3["structured answer: Checklist"]:::out
    S2 --> S3
    Z(["typed result"])
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
| `pr_facts` | Facts about a PR. | read-only | - |

## Skills

`/skills/pr-checklist/SKILL.md`: Use for merge readiness.

1. Tests changed
2. Migrations have down scripts
3. Docs updated for API changes

## Run it

```bash
python usecases/swe_day/044_pr_checklist_skill/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/044_pr_checklist_skill/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `pull_request.opened` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- The `Checklist` result is a Pydantic object, so you can post it straight to a dashboard or database.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
