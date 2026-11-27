# 052. Customer escalation investigation

**When:** 14:00 (ops)  
**Trigger:** `webhook: support_escalation`  
**Type:** investigation  
**Deep Agents features:** parallel calls

Pulls the payment events and logs and writes up what actually happened for support.

## What you ask

> Customer says they were charged twice for order 99812. Investigate.

## Flow

```mermaid
flowchart TD
    T(["webhook: support_escalation"]) --> A["Deep Agent"]
    S1["payment_events"]:::tool
    S2["request_logs"]:::tool
    A --> S1
    A --> S2
    Z(["answer to you"])
    S1 --> Z
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
| `payment_events` | Payment events for an order. | read-only | - |
| `request_logs` | Request logs for an order. | read-only | - |

## Run it

```bash
python usecases/swe_day/052_customer_escalation_investigation/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/052_customer_escalation_investigation/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `support_escalation` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
