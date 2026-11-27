# 056. Answer a product question from the code

**When:** 14:35 (ops)  
**Trigger:** `slack: #ask-payments`  
**Type:** Q&A  
**Deep Agents features:** 

Answers from the actual code, with the file and line, not from what someone remembers.

## What you ask

> PM asks: do we retry failed webhooks, and how many times?

## Flow

```mermaid
flowchart TD
    T(["slack: ask-payments"]) --> A["Deep Agent"]
    S1["search_code"]:::tool
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
| `search_code` | Search code. | read-only | - |

## Run it

```bash
python usecases/swe_day/056_answer_product_question_from_code/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/056_answer_product_question_from_code/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Wire it to Slack (#ask-payments) with Slack Bolt; use the Slack thread id as the LangGraph `thread_id`.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
