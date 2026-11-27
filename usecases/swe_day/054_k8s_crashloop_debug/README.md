# 054. Kubernetes CrashLoopBackOff debug

**When:** 14:15 (ops)  
**Trigger:** `webhook: pod_crashloop`  
**Type:** troubleshooting  
**Deep Agents features:** parallel calls

Reads pod events and previous logs, finds the cause, suggests the fix.

## What you ask

> ledger-worker is in CrashLoopBackOff.

## Flow

```mermaid
flowchart TD
    T(["webhook: pod_crashloop"]) --> A["Deep Agent"]
    S1["pod_events"]:::tool
    S2["previous_logs"]:::tool
    S3["pod_limits"]:::tool
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
| `pod_events` | kubectl describe events. | read-only | - |
| `previous_logs` | kubectl logs --previous. | read-only | - |
| `pod_limits` | Resource limits. | read-only | - |

## Run it

```bash
python usecases/swe_day/054_k8s_crashloop_debug/usecase.py            # offline: scripted model, real Deep Agent
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/054_k8s_crashloop_debug/usecase.py --live   # a real model makes the decisions
```

## Taking it to production

- Start it from the `pod_crashloop` webhook. A small FastAPI endpoint that calls `agent.invoke(...)` with a fresh `thread_id` per event is enough.
- Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).
