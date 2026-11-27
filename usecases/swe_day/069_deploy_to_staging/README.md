# 069. Deploy to staging

**When:** 16:20 (release)  
**Trigger:** `webhook: tag.pushed`  
**Type:** deploy  
**Deep Agents features:** guardrail

Staging deploys are self-serve; the guard stops the agent pointing the same tool at prod.

## What you ask

> Deploy v2.32.0 to staging.

## Flow

```mermaid
flowchart TD
    T(["webhook: tag.pushed"]) --> A["Deep Agent"]
    S1["deploy (policy guard)"]:::guard
    A --> S1
    Z(["answer to you"])
    S1 --> Z
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
| `deploy` | Deploy a version to an environment. | changes state | policy guard |

## Run it

```bash
python usecases/swe_day/069_deploy_to_staging/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/069_deploy_to_staging/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `tag.pushed` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- Keep the guard. It's ordinary Python in middleware, so it holds even when the model gets it wrong.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
