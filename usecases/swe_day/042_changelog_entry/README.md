# 042. Changelog entry from a PR

**When:** 12:55 (review)  
**Trigger:** `webhook: pull_request.labeled`  
**Type:** docs  
**Deep Agents features:** filesystem

Keeps CHANGELOG.md in Keep-a-Changelog format without anyone thinking about it.

## What you ask

> Add a changelog entry for PR #812.

## Flow

```mermaid
flowchart TD
    T(["webhook: pull_request.labeled"]) --> A["Deep Agent"]
    S1["get_pr"]:::tool
    A --> S1
    S2["read /repo/CHANGELOG.md"]:::file
    S1 --> S2
    S3["edit /repo/CHANGELOG.md"]:::file
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
| `get_pr` | PR metadata. | read-only | - |

## Run it

```bash
python usecases/swe_day/042_changelog_entry/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/042_changelog_entry/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `pull_request.labeled` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
