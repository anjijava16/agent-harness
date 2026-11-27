# 022. Find who owns the code you're about to change

**When:** 09:55 (planning)  
**Trigger:** `manual`  
**Type:** lookup  
**Deep Agents features:** filesystem

Combines CODEOWNERS with recent git history so you tag the right people.

## What you ask

> Who should review changes to payments/store.py?

## Flow

```mermaid
flowchart TD
    T(["manual"]) --> A["Deep Agent"]
    S1["read /repo/CODEOWNERS"]:::file
    A --> S1
    S2["git_log_authors"]:::tool
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
| `git_log_authors` | Top recent authors of a file. | read-only | - |

## Run it

```bash
python usecases/swe_day/022_find_code_owners/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/022_find_code_owners/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- You start this one yourself: a CLI command, a Slack slash command or an IDE action.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
