# 038. Local environment troubleshooting

**When:** 12:28 (coding)  
**Trigger:** `manual`  
**Type:** troubleshooting  
**Deep Agents features:** filesystem

Reads the error and compose file, finds the conflict, suggests the exact fix.

## What you ask

> docker compose up fails on my machine. Help.

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["compose_logs"]:::tool
    A --> S1
    S2["read /repo/docker-compose.yml"]:::file
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
| `compose_logs` | docker compose logs. | read-only | - |

## Run it

```bash
python usecases/swe_day/038_local_env_troubleshooting/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/038_local_env_troubleshooting/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
