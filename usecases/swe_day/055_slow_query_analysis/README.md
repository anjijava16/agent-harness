# 055. Slow query analysis

**When:** 14:25 (ops)  
**Trigger:** `webhook: db_slow_query_alert`  
**Type:** performance  
**Deep Agents features:** structured output

Runs EXPLAIN through a read-only tool and recommends an index.

## What you ask

> This query on invoices takes 4s. Why?

## Flow

```mermaid
flowchart TD
    T(["webhook: db_slow_query_alert"]) --> A["Deep Agent"]
    S1["explain"]:::tool
    A --> S1
    S2["structured answer: QueryFix"]:::out
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
| `explain` | EXPLAIN ANALYZE a query (read-only replica). | read-only | - |

## Run it

```bash
python usecases/swe_day/055_slow_query_analysis/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/055_slow_query_analysis/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `db_slow_query_alert` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- The `QueryFix` result is a Pydantic object, so you can post it straight to a dashboard or database.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
