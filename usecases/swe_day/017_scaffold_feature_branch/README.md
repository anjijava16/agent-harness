# 017. Scaffold a feature from the service template

**When:** 09:10 (planning)  
**Trigger:** `manual`  
**Type:** scaffolding  
**Deep Agents features:** filesystem

Reads the team's template files and writes the new module skeleton so you start from conventions, not a blank page.

## What you ask

> Scaffold the invoice-export module from our template.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["create_branch"]:::tool
    A --> S1
    S2["read /templates/module/service.py"]:::file
    S1 --> S2
    S3["write /repo/payments/invoice_export/service.py"]:::file
    S2 --> S3
    S4["write /repo/payments/invoice_export/test_se..."]:::file
    S3 --> S4
    Z(["answer to you"])
    S4 --> Z
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
| `create_branch` | Create a git branch. | changes state | - |

## Run it

```bash
python usecases/swe_day/017_scaffold_feature_branch/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/017_scaffold_feature_branch/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
