# 018. Design doc first draft

**When:** 09:20 (planning)  
**Trigger:** `manual`  
**Type:** doc drafting  
**Deep Agents features:** skills, filesystem

Follows the team's design-doc skill so every doc has the same sections reviewers expect.

## What you ask

> Draft a design doc for idempotency keys.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["read /skills/design-doc/SKILL.md"]:::file
    A --> S1
    S2["get_ticket"]:::tool
    S1 --> S2
    S3["write /docs/design/idempotency_keys.md"]:::file
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
| `get_ticket` | Fetch a ticket. | read-only | - |

## Skills

`/skills/design-doc/SKILL.md`: Use when writing design docs.

1. Context
2. Goals / non-goals
3. Design
4. Alternatives
5. Rollout
6. Risks

## Run it

```bash
python usecases/swe_day/018_design_doc_first_draft/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/018_design_doc_first_draft/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
