# 014. Acceptance criteria generator

**When:** 08:40 (planning)  
**Trigger:** `manual`  
**Type:** ticket refinement  
**Deep Agents features:** structured output

Turns a vague ticket into testable Given/When/Then criteria in a fixed schema.

## What you ask

> Write acceptance criteria for 'export invoices as CSV'.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["get_ticket"]:::tool
    A --> S1
    S2["structured answer: AcceptanceCriteria"]:::out
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
| `get_ticket` | Fetch a ticket. | read-only | - |

## Run it

```bash
python usecases/swe_day/014_acceptance_criteria_generator/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/014_acceptance_criteria_generator/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- The `AcceptanceCriteria` result is a Pydantic object, so you can post it straight to a dashboard or database.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
