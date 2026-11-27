# 070. Smoke tests on staging

**When:** 16:30 (release)  
**Trigger:** `webhook: deploy.succeeded(staging)`  
**Type:** testing  
**Deep Agents features:** parallel calls

Runs the suites in parallel and reports only what matters.

## What you ask

> Run smoke tests against staging.

## Flow

```mermaid
flowchart TD
    T(["webhook: deploy.succeeded(staging)"]) --> A["Deep Agent"]
    S1["smoke"]:::tool
    S2["smoke"]:::tool
    S3["smoke"]:::tool
    A --> S1
    A --> S2
    A --> S3
    Z(["answer to you"])
    S1 --> Z
    S2 --> Z
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
| `smoke` | Run a smoke suite. | read-only | - |

## Run it

```bash
python usecases/swe_day/070_staging_smoke_tests/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/070_staging_smoke_tests/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `deploy.succeeded(staging)` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
