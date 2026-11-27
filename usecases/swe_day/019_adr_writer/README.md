# 019. Architecture decision record

**When:** 09:30 (planning)  
**Trigger:** `manual`  
**Type:** doc drafting  
**Deep Agents features:** filesystem

Captures a decision in the repo's ADR format while the reasoning is fresh.

## What you ask

> Write an ADR for choosing Arq for background jobs.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["ls /repo/docs/adr"]:::file
    A --> S1
    S2["next_adr_number"]:::tool
    S1 --> S2
    S3["write /repo/docs/adr/0017-arq-for-backgroun..."]:::file
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
| `next_adr_number` | Next ADR number in the repo. | read-only | - |

## Run it

```bash
python usecases/swe_day/019_adr_writer/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/019_adr_writer/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
