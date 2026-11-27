# 064. Reproduce a bug from a support ticket

**When:** 15:45 (ops)  
**Trigger:** `webhook: zendesk_ticket_tagged_bug`  
**Type:** bug repro  
**Deep Agents features:** filesystem

Writes a failing test that reproduces the report; the fix comes after.

## What you ask

> Support says invoices with emoji in the name fail to export. Reproduce it.

## Flow

```mermaid
flowchart TD
    T(["webhook: zendesk_ticket_tagged_bug"]) --> A["Deep Agent"]
    S1["get_support_ticket"]:::tool
    A --> S1
    S2["write /repo/tests/test_export_unicode.py"]:::file
    S1 --> S2
    S3["run_tests"]:::tool
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
| `get_support_ticket` | Support ticket. | read-only | - |
| `run_tests` | Run tests. | read-only | - |

## Run it

```bash
python usecases/swe_day/064_support_ticket_reproduction/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/064_support_ticket_reproduction/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `zendesk_ticket_tagged_bug` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
