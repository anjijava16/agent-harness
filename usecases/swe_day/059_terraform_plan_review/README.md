# 059. Terraform plan review

**When:** 15:05 (ops)  
**Trigger:** `webhook: atlantis_plan`  
**Type:** infra review  
**Deep Agents features:** guardrail

Applies are blocked whenever the plan destroys a stateful resource.

## What you ask

> Review the Terraform plan for the payments VPC change and apply if safe.

## Flow

```mermaid
flowchart TD
    T(["webhook: atlantis_plan"]) --> A["Deep Agent"]
    S1["tf_plan"]:::tool
    A --> S1
    S2["tf_apply (policy guard)"]:::guard
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
| `tf_plan` | Terraform plan summary. | read-only | - |
| `tf_apply` | Terraform apply. | changes state | policy guard |

## Run it

```bash
python usecases/swe_day/059_terraform_plan_review/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/059_terraform_plan_review/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `atlantis_plan` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- Keep the guard. It's ordinary Python in middleware, so it holds even when the model gets it wrong.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
