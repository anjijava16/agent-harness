# 037. Dockerfile size and build-time optimization

**When:** 12:25 (coding)  
**Trigger:** `manual`  
**Type:** build  
**Deep Agents features:** filesystem

Reads the Dockerfile, rewrites it as a multi-stage build, checks size with a tool.

## What you ask

> Make the payments-api image smaller.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["read /repo/Dockerfile"]:::file
    A --> S1
    S2["write /repo/Dockerfile"]:::file
    S1 --> S2
    S3["image_size"]:::tool
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
| `image_size` | Build an image and report its size. | read-only | - |

## Run it

```bash
python usecases/swe_day/037_dockerfile_optimization/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/037_dockerfile_optimization/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
