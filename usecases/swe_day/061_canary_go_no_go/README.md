# 061. Canary go / no-go

**When:** 15:25 (ops)  
**Trigger:** `webhook: canary_window_complete`  
**Type:** deploy decision  
**Deep Agents features:** AGENTS.md, structured output

Compares canary and baseline metrics against fixed thresholds and returns a typed verdict.

## What you ask

> Is the ledger v3.2 canary good to promote?

## Flow

```mermaid
flowchart TD
    T(["webhook: canary_window_complete"]) --> A["Deep Agent"]
    S1["canary_compare"]:::tool
    A --> S1
    S2["structured answer: CanaryVerdict"]:::out
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
| `canary_compare` | Canary vs baseline metrics. | read-only | - |

## House rules (AGENTS.md)

```markdown
# Canary rules
No-go if error rate > 1.5x baseline or p99 > 1.2x baseline.
```

## Run it

```bash
python usecases/swe_day/061_canary_go_no_go/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/061_canary_go_no_go/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `canary_window_complete` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- The `CanaryVerdict` result is a Pydantic object, so you can post it straight to a dashboard or database.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
