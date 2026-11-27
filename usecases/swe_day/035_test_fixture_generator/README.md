# 035. Generate realistic test fixtures

**When:** 12:15 (coding)  
**Trigger:** `manual`  
**Type:** test data  
**Deep Agents features:** filesystem

Reads the model definition so fixtures match the schema.

## What you ask

> Generate 5 invoice fixtures covering paid, overdue and disputed.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["read /repo/payments/models.py"]:::file
    A --> S1
    S2["write /repo/tests/fixtures/invoices.json"]:::file
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
| (none) | Only the built-in Deep Agents file tools | - | - |

## Run it

```bash
python usecases/swe_day/035_test_fixture_generator/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/035_test_fixture_generator/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
