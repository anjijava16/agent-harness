# **Production-Ready Deep Agent Harness Using Google ADK**



Recommended architecture

Python

Enterprise / Production



My recommendation is to build a reusable **Enterprise Deep Agent Harness on Google ADK**, rather than migrate your existing supervisor and specialized agents to LangChain Deep Agents.

Your existing supervisor-based architecture is already a strong foundation. The next step is to add a durable execution layer, context-engineering layer, workspace, memory, recovery mechanisms and observability around it.

The key architectural principle:

> An agent should not need to remember everything, execute everything in one session, or finish everything in one uninterrupted model call. The harness should manage the lifecycle, context, state, delegation and recovery.

I would design this around six core subsystems:

1. Agent orchestration and planning.
2. Context engineering and memory.
3. Durable task execution and checkpointing.
4. Workspace and artifact management.
5. MCP and A2A integration.
6. Observability, security and governance.

## **1. Target enterprise architecture**

I recommend a layered architecture with Google ADK as the runtime and your own harness as the reusable enterprise control plane.

## **Enterprise Deep Agent Harness**

**Enterprise Client Layer**

REST API • FastAPI • WebSocket • UI • Enterprise applications

**1. Harness API / Runtime Gateway**

Authentication • Tenant isolation • Request validation • Run creation • Idempotency

## **2. Agent Orchestration — Google ADK**

**Supervisor Agent**

Intent classification • Planning • Delegation • Synthesis

**Research Agent**

RAG and discovery

**Data Agent**

SQL and analytics

**Execution Agent**

Business operations

**Validation Agent**

Quality and compliance

**3. Context Engine**

Context selection, summarization, memory, retrieval

**4. Durable Execution**

Task queue, checkpoints, retries, resume

**5. Workspace**

Files, artifacts, intermediate outputs

**6. Governance**

Approval, permissions, policies, audit

**Integration Layer**

- MCP servers — tools and enterprise resources
- A2A — remote agent collaboration
- APIs — databases, internal services and applications

**Infrastructure and Platform**

Cloud SQL / PostgreSQL • Redis • Pub/Sub or Cloud Tasks • Cloud Storage • OpenTelemetry • Cloud Logging

### **Important architectural decision**

Do not put all functionality inside the supervisor's prompt.

Keep the supervisor responsible for decisions and delegation. Put durable execution, memory, checkpoints, context assembly and policy enforcement into separate services.

This makes the harness reusable across different agent teams and business domains.

## **2. Google ADK component mapping**

Here is how I would implement each subsystem.

| Harness subsystem         | Google ADK component         | Additional implementation    |
| ------------------------- | ---------------------------- | ---------------------------- |
| Agent runtime             | `Runner`                     | Runtime gateway              |
| Application configuration | `App`                        | Harness configuration        |
| Supervisor                | `LlmAgent`                   | Planning policy              |
| Specialized agents        | `LlmAgent`                   | Domain instructions          |
| Workflow                  | `Workflow` / workflow nodes  | Dependency management        |
| Agent delegation          | Agent transfer / `AgentTool` | Delegation policy            |
| Short-term state          | `SessionService`             | State schema                 |
| Persistent user memory    | `MemoryService`              | Retrieval strategy           |
| Large files               | `ArtifactService`            | GCS workspace                |
| Long-running tools        | `LongRunningFunctionTool`    | Task worker and queue        |
| Tool connectivity         | `McpToolset`                 | MCP gateway                  |
| Remote agents             | `RemoteA2aAgent`             | Agent discovery and registry |
| Observability             | ADK plugins and telemetry    | OpenTelemetry backend        |

**Version consideration:** Google's current ADK Python documentation also describes newer `Workflow` and `BaseNode` abstractions. Avoid assuming that every older `SequentialAgent`, `ParallelAgent` or `LoopAgent` tutorial represents the newest workflow API. Pin your ADK version and test against its matching documentation.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+2



## **3. Context engineering — the most important subsystem**

This is where I would invest most of your engineering effort.

A common production failure is that agents keep receiving the entire conversation history, every tool output and every intermediate result.

This causes:

- Token consumption to grow.
- Important instructions to get buried.
- Context-window exhaustion.
- Repeated retrieval and reasoning.
- Poor performance on long-running tasks.

Instead, implement a **four-tier context architecture**.

## **Four-tier context architecture**

**Tier 1 — Working Context**

Immediate

Current task, relevant instructions, selected history, tool outputs and next action.

**Tier 2 — Session Context**

Conversation

Session state, execution status, decisions, task dependencies and checkpoints.

**Tier 3 — Persistent Memory**

Long-term

Important facts, preferences, previous decisions, domain knowledge and reusable learnings.

**Tier 4 — External Workspace**

On demand

Documents, source code, research reports, datasets, logs and intermediate artifacts.

Google ADK supports this separation through sessions, state, memory, artifacts and context assembly. Its Context interface provides access to these resources.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1



### **3.1 What should be stored where?**

| Data                      | Storage                 | Example                     |
| ------------------------- | ----------------------- | --------------------------- |
| Current reasoning inputs  | Working context         | Current user request        |
| Current execution status  | Session state / task DB | Research completed          |
| Cross-session preferences | Memory                  | User prefers SQL            |
| Large research results    | Artifact storage        | Research report PDF         |
| Task dependencies         | Task DB                 | Analysis waits for research |
| Execution history         | ADK events / audit DB   | Tool invocation             |
| Sensitive credentials     | Secret manager          | API credentials             |

**Critical rule:** Do not store the entire task history in the model's prompt. Store structured execution data externally and retrieve only what the current agent needs.

### **3.2 Context assembly pipeline**

For every agent invocation, I recommend this pipeline:

**1**

Identify task and agent identity

**2**

Load execution state and task dependencies

**3**

Retrieve relevant memory and workspace references

**4**

Select the most useful conversation history

**5**

Apply token budget and context summarization

**6**

Add instructions, policies and tool descriptions

**7**

Invoke the model and capture the result

**8**

Persist decisions, artifacts and state changes

### **3.3 Context budget example**

Suppose your selected model has a 128K-token context window. You could initially allocate:

| Component                            | Example budget |
| ------------------------------------ | -------------- |
| System instructions and policies     | 8K             |
| Task and execution state             | 8K             |
| Relevant history                     | 16K            |
| Retrieved documents                  | 32K            |
| Tool descriptions and outputs        | 16K            |
| Current reasoning / response reserve | 48K            |
| **Total**                            | **128K**       |

These are illustrative budgets, not universal settings. Configure them per model, task and agent.

### **3.4 ADK context compaction**

Use ADK's `EventsCompactionConfig` to prevent unbounded event history from entering the working context.

For example, in versions exposing this API:

```
from google.adk.apps import Appfrom google.adk.apps import EventsCompactionConfigapp = App(    name="enterprise_harness",    root_agent=root_agent,    events_compaction_config=EventsCompactionConfig(        compaction_interval=5,        overlap_size=2,    ),)
```

Treat the values as starting examples, not production defaults. Validate the constructor and summarization behavior against your pinned ADK release.

One important distinction: compaction reduces conversation history. It is not a replacement for durable task state. Your critical execution facts must live in structured storage.

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1

## **4. Long-running task management and recovery**

This is the second major investment area.

Imagine an enterprise request:

> Analyze 500 customer accounts, retrieve transaction histories, identify unusual patterns, generate risk reports, validate the results and produce a consolidated executive report.

This could take 20 minutes, several hours or even days depending on external systems and approval requirements.

You should not run this as one continuous agent invocation.

### **4.1 Introduce a durable task execution engine**

Create an independent task lifecycle:

## **Long-running execution lifecycle**

**REQUESTED**

**PLANNING**

Create tasks and dependencies

**QUEUED**

Persist task and dispatch work

**EXECUTING**

Research

Completed

Transactions

Running

Risk analysis

Waiting

Validation

Waiting

**WAITING**

Approval / external event

**RETRY**

Recoverable failure

**COMPLETED**

Validated output and final artifacts

### **4.2 Recommended task database schema**

Use PostgreSQL or Cloud SQL as the durable source of truth.

**Table: agent_runs**

| Column       | Purpose                     |
| ------------ | --------------------------- |
| run_id       | Unique execution identifier |
| tenant_id    | Enterprise tenant           |
| user_id      | Request owner               |
| session_id   | ADK session                 |
| status       | Run lifecycle               |
| root_task_id | Main task                   |
| created_at   | Creation time               |
| updated_at   | Last update                 |

**Table: agent_tasks**

| Column          | Purpose              |
| --------------- | -------------------- |
| task_id         | Unique task          |
| run_id          | Parent run           |
| parent_task_id  | Parent task          |
| assigned_agent  | Specialized agent    |
| input_ref       | Input artifact       |
| output_ref      | Output artifact      |
| status          | Task status          |
| retry_count     | Retry attempts       |
| checkpoint_ref  | Last checkpoint      |
| idempotency_key | Duplicate prevention |

**Table: agent_events**

- Task started.
- Agent delegated.
- Tool executed.
- Artifact created.
- Checkpoint saved.
- Approval requested.
- Task resumed.
- Task completed or failed.

Keep business-level task events distinct from ADK conversation events. This gives you a stable audit trail even if you change agent frameworks later.

### **4.3 Execution design**

I recommend:

- Cloud Tasks or Pub/Sub for asynchronous task dispatch.
- PostgreSQL / Cloud SQL for execution state.
- Cloud Storage for large artifacts.
- ADK Runner for agent execution.
- A dedicated worker service for task processing.

Use the transactional outbox pattern when writing task records and scheduling messages. It prevents a database commit succeeding while the corresponding queue message is lost.

**Important:** Persisting an ADK session does not automatically make an in-flight Python process durable. Your external worker must be able to reconstruct execution from persisted state. ADK resumability can help with supported pause/resume scenarios, but it does not replace your task ledger and recovery design.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+3



### **4.4 Python implementation: task contract**

I would create a framework-independent task contract.

```
from enum import StrEnumfrom pydantic import BaseModel, Fieldfrom datetime import datetimefrom typing import Anyclass TaskStatus(StrEnum):    REQUESTED = "requested"    PLANNING = "planning"    QUEUED = "queued"    RUNNING = "running"    WAITING = "waiting"    RETRY = "retry"    COMPLETED = "completed"    FAILED = "failed"    CANCELLED = "cancelled"class AgentTask(BaseModel):    task_id: str    run_id: str    parent_task_id: str | None = None    assigned_agent: str    description: str    status: TaskStatus = TaskStatus.REQUESTED    input_ref: str | None = None    output_ref: str | None = None    checkpoint_ref: str | None = None    retry_count: int = 0    idempotency_key: str    created_at: datetime    updated_at: datetime    metadata: dict[str, Any] = Field(default_factory=dict)
```

### **4.5 Worker execution pattern**

```
        return    try:        # 2. Load durable execution context.        run = await run_store.get(task.run_id)        # 3. Reconstruct the ADK session.        session = await session_manager.load(            session_id=run.session_id,            user_id=run.user_id,        )        # 4. Load only the context required by this task.        context = await context_engine.build(            task=task,            run=run,            session=session,        )        # 5. Execute the assigned ADK agent.        result = await adk_executor.execute(            agent_name=task.assigned_agent,            context=context,        )        # 6. Persist output before marking complete.        artifact_ref = await artifact_store.save(result)        await task_store.complete(            task_id=task.task_id,            output_ref=artifact_ref,        )    except RetryableError as exc:        await task_store.schedule_retry(            task_id=task_id,            error=str(exc),        )    except Exception as exc:        await task_store.fail(            task_id=task_id,            error=str(exc),        )        raise
```

This is a reference orchestration pattern, not a drop-in ADK API. The `task_store`, `context_engine` and `adk_executor` are services you implement.

### **4.6 Critical reliability controls**

| Problem                       | Solution                                  |
| ----------------------------- | ----------------------------------------- |
| Worker crashes                | Reclaim expired task leases               |
| Duplicate delivery            | Idempotency keys                          |
| API timeout                   | Asynchronous execution                    |
| Model timeout                 | Bounded retries                           |
| Context overflow              | Compaction and selective retrieval        |
| Agent failure                 | Checkpoint and reassign                   |
| External API failure          | Exponential backoff                       |
| Duplicate financial operation | Idempotent business transaction           |
| Human approval pending        | Persist waiting state and resume on event |

For business operations, never assume that retrying an agent tool call is harmless. Use idempotency keys and external transaction-status verification.

## **5. MCP and A2A integration strategy**

You should use both protocols, but for different purposes.

# **MCP**

Tool connectivity

**Model Context Protocol**

Connect your ADK agents to enterprise tools and resources.

Examples:

- Database MCP server.
- Internal API MCP server.
- GitHub MCP server.
- Enterprise search MCP server.
- Observability MCP server.

# **A2A**

Agent interoperability

**Agent2Agent protocol**

Allow independent agents and services to collaborate.

Examples:

- ADK research agent communicates with an external risk agent.
- A remote Java agent performs an enterprise operation.
- Another team exposes an independent agent service.
- External agents return structured task results.

### **5.1 MCP implementation with Google ADK**

Example pattern:

```
from google.adk.agents import LlmAgentfrom google.adk.tools.mcp_tool import MCPToolsetfrom google.adk.tools.mcp_tool import StreamableHTTPConnectionParamsenterprise_mcp = MCPToolset(    connection_params=StreamableHTTPConnectionParams(        url="https://mcp.internal.example.com/mcp",        headers={            "Authorization": "Bearer <runtime-token>"        },    ),)data_agent = LlmAgent(    name="enterprise_data_agent",    model="YOUR_SUPPORTED_MODEL",    instruction="""    You are an enterprise data specialist.    Retrieve only authorized data.    Validate the results before returning them.    """,    tools=[enterprise_mcp],)
```

This illustrates a Streamable HTTP MCP connection. Adapt the connection and authentication setup to your installed ADK release. Do not hardcode production tokens in source code.

**Enterprise MCP recommendations:**

- Separate read and write toolsets.
- Enforce authorization at the MCP server, not just in agent instructions.
- Apply per-tenant tool filtering.
- Set timeouts and output-size limits.
- Audit every sensitive tool invocation.
- Require human confirmation for high-impact operations.

### **5.2 A2A integration**

Use A2A when the other agent is independently deployed and needs to maintain its own identity, execution and lifecycle.

A typical architecture:

**ADK Supervisor**

**Local ADK Agent**

Research

**Remote A2A Agent**

Risk analysis

**Local ADK Agent**

Validation

**Remote A2A Agent**

Compliance

For remote agents, your harness should maintain:

- Agent discovery and capability registry.
- Agent identity and authorization.
- A2A task ID to internal run/task ID mapping.
- Timeout and retry policies.
- Result validation.
- Trace correlation.
- Cancellation and status handling.

ADK provides A2A-related components for exposing agents and consuming remote agents.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1



**My rule:** MCP for capabilities; A2A for independent agent collaboration. Don't use A2A merely to call a local Python function.

## **6. Observability: make every agent execution traceable**

For enterprise production, observability should be built into the harness from day one.

You need to answer:

- Why did the supervisor delegate to this agent?
- What context did the agent receive?
- Which MCP tools were invoked?
- How long did each model call take?
- Which subagent failed?
- How many tokens were consumed?
- What caused a retry?
- What was the last successful checkpoint?
- Did the agent produce a verified result?

### **6.1 Observability architecture**

**Google ADK Runtime**

Supervisor • Subagents • Tools • Workflows

**Instrumentation Layer**

ADK Plugins • Callbacks • OpenTelemetry • Custom spans

**Traces**

Agent execution, delegation, tools

**Metrics**

Latency, tokens, failures, cost

**Logs**

Execution and error details

**Evaluations**

Quality, groundedness, task success

**Observability Platform**

Cloud Trace • Cloud Monitoring • Cloud Logging • BigQuery / dashboards

### **6.2 Trace hierarchy**

For one enterprise request, I would capture a trace similar to:

```
enterprise.run
│
├── harness.context_assembly
│
├── supervisor.plan
│
├── supervisor.delegate
│   ├── research_agent.execute
│   │   ├── llm.generate
│   │   └── mcp.search
│   │
│   ├── data_agent.execute
│   │   ├── llm.generate
│   │   └── mcp.query
│   │
│   ├── analysis_agent.execute
│   │   └── llm.generate
│   │
│   └── validation_agent.execute
│
├── harness.checkpoint
├── harness.context_compaction
└── enterprise.run.complete
```

### **6.3 Recommended telemetry fields**

| Field            | Purpose                 |
| ---------------- | ----------------------- |
| `trace_id`       | Entire request          |
| `run_id`         | Durable execution       |
| `task_id`        | Individual task         |
| `session_id`     | ADK session             |
| `agent_name`     | Executing agent         |
| `parent_task_id` | Delegation relationship |
| `model_name`     | Model used              |
| `tool_name`      | Tool invoked            |
| `input_tokens`   | Token consumption       |
| `output_tokens`  | Token consumption       |
| `latency_ms`     | Execution duration      |
| `retry_count`    | Retry count             |
| `status`         | Execution status        |
| `artifact_ref`   | Output reference        |

Use OpenTelemetry trace context propagation across FastAPI, worker processes, MCP services and A2A calls.

ADK provides plugins and telemetry integration points. Add custom spans around your harness-specific context and task services.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+2



### **6.4 Production KPIs**

I would monitor these metrics:

| Metric                    | What it tells you       |
| ------------------------- | ----------------------- |
| Task completion rate      | Reliability             |
| Successful resume rate    | Recovery quality        |
| Agent delegation success  | Orchestration quality   |
| Context retrieval latency | Context performance     |
| Context tokens per task   | Context efficiency      |
| Tool failure rate         | Integration reliability |
| Human approval wait time  | Process bottlenecks     |
| Cost per completed run    | Financial efficiency    |
| Groundedness score        | Response reliability    |
| P95 execution latency     | User experience         |

Never export raw prompts, personal information, access tokens or confidential tool outputs into telemetry by default. Use redaction, restricted access and configurable sampling.

## **7. Python project structure**

I would organize the codebase as a reusable framework, not a collection of agent scripts.

```
enterprise-agent-harness/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── runs.py
│   │   ├── tasks.py
│   │   └── approvals.py
│   │
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── planner.py
│   │   ├── research_agent.py
│   │   ├── data_agent.py
│   │   ├── execution_agent.py
│   │   └── validation_agent.py
│   │
│   ├── harness/
│   │   ├── runtime.py
│   │   ├── lifecycle.py
│   │   ├── delegation.py
│   │   ├── task_manager.py
│   │   ├── checkpoint.py
│   │   ├── recovery.py
│   │   └── policy.py
│   │
│   ├── context/
│   │   ├── context_builder.py
│   │   ├── context_budget.py
│   │   ├── compaction.py
│   │   ├── retrieval.py
│   │   └── memory.py
│   │
│   ├── integrations/
│   │   ├── mcp/
│   │   ├── a2a/
│   │   └── enterprise_apis/
│   │
│   ├── storage/
│   │   ├── sessions.py
│   │   ├── tasks.py
│   │   ├── artifacts.py
│   │   └── repositories.py
│   │
│   ├── observability/
│   │   ├── tracing.py
│   │   ├── metrics.py
│   │   ├── logging.py
│   │   └── evaluation.py
│   │
│   └── config/
│       ├── settings.py
│       └── agent_registry.py
│
├── workers/
│   ├── task_worker.py
│   └── recovery_worker.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── evaluations/
│   ├── reliability/
│   └── load/
│
├── Dockerfile
├── pyproject.toml
└── README.md
```

### **7.1 Supervisor implementation example**

Here is a starting point using ADK's agent hierarchy.

```
from google.adk.agents import LlmAgentfrom app.agents.research_agent import research_agentfrom app.agents.data_agent import data_agentfrom app.agents.analysis_agent import analysis_agentfrom app.agents.validation_agent import validation_agentsupervisor = LlmAgent(    name="enterprise_supervisor",    model="YOUR_SUPPORTED_MODEL",    instruction="""    You are the enterprise task supervisor.    Responsibilities:    1. Understand the business request.    2. Break complex requests into manageable tasks.    3. Identify dependencies between tasks.    4. Delegate work to specialized agents.    5. Validate agent outputs.    6. Synthesize a final response.    Context management:    - Never assume all previous context is available.    - Use persisted task state and artifact references.    - Request only the information needed by each agent.    - Do not invent task completion status.    Long-running tasks:    - Delegate independent work in parallel where supported.    - Do not mark a task complete until its output is persisted.    - Escalate sensitive operations for approval.    """,
```

This is the ADK-style agent hierarchy. The durable planner, task graph and recovery mechanisms should remain in your harness services rather than being entrusted entirely to LLM instructions.

### **7.2 Specialized agent contract**

Every agent should return a predictable result.

```
from pydantic import BaseModel, Fieldfrom typing import Literalclass AgentResult(BaseModel):    task_id: str    agent_name: str    status: Literal[        "completed",        "waiting",        "failed",    ]    summary: str    artifact_refs: list[str] = Field(        default_factory=list    )    evidence_refs: list[str] = Field(        default_factory=list    )    errors: list[str] = Field(        default_factory=list    )    next_actions: list[str] = Field(        default_factory=list    )
```

This makes agent outputs easier to validate, persist, pass between agents and evaluate.

## **8. Google Cloud deployment architecture**

For your Google ADK and FastAPI experience, I would use this deployment model.

## **Google Cloud production deployment**

**API Gateway / Load Balancer**

**Cloud Run — Harness API**

FastAPI • Authentication • Run management

**Cloud Run**

ADK Supervisor

**Cloud Run**

Agent Workers

**Cloud Run**

MCP Services

**Cloud Run**

A2A Services

**Managed infrastructure**

**Cloud SQL**

Task state

**Cloud Storage**

Artifacts

**Pub/Sub**

Event dispatch

**Redis**

Cache / coordination

**Secret Manager**

Credentials

**BigQuery**

Analytics

**Cloud Trace • Cloud Monitoring • Cloud Logging**

### **Deployment recommendations**

| Component          | Recommended platform                                  |
| ------------------ | ----------------------------------------------------- |
| Harness REST API   | Cloud Run                                             |
| ADK supervisor     | Cloud Run                                             |
| Specialized agents | Cloud Run or shared worker service                    |
| Async execution    | Pub/Sub / Cloud Tasks                                 |
| Session storage    | Cloud SQL or supported ADK persistent session service |
| Task state         | Cloud SQL PostgreSQL                                  |
| Artifacts          | Cloud Storage                                         |
| Memory             | ADK MemoryService with appropriate persistent backend |
| MCP                | Cloud Run                                             |
| A2A                | Cloud Run                                             |
| Secrets            | Secret Manager                                        |
| Observability      | OpenTelemetry + Google Cloud observability            |

For high-throughput workloads, consider GKE when you need more control over worker scheduling, networking, isolation or compute-intensive execution.

For managed agent execution, also evaluate Vertex AI Agent Engine. It can change which session, memory, sandbox and deployment responsibilities you need to operate yourself.

## **9. Security and enterprise governance**

In an enterprise environment, especially when agents can access business systems, I would make these mandatory.

| Control          | Implementation                                |
| ---------------- | --------------------------------------------- |
| Authentication   | OAuth2 / OIDC                                 |
| Authorization    | RBAC + ABAC                                   |
| Tenant isolation | Tenant-scoped sessions and artifacts          |
| Tool permissions | Per-agent allowlists                          |
| Secrets          | Google Secret Manager                         |
| Data protection  | Encryption at rest and in transit             |
| Prompt injection | Input screening and trusted-source boundaries |
| Human approval   | Explicit approval for high-impact operations  |
| Audit            | Immutable business activity records           |
| Model governance | Approved model registry                       |
| Data leakage     | PII redaction and output validation           |
| Code execution   | Isolated sandbox                              |

One architectural rule is particularly important:

**Never allow an LLM to determine its own authorization.**

The harness and external services must enforce permissions independently of model-generated decisions.

## **10. Implementation roadmap: 8 weeks**

I would implement this incrementally, keeping your existing ADK agents operational.

## **Enterprise harness delivery plan**

1. **Weeks 1–2: Core harness**
   - Standardize agent interfaces.
   - Introduce supervisor and task contracts.
   - Implement run and task lifecycle.
   - Introduce PostgreSQL persistence.

     Deliverable: Core runtime
2. **Weeks 3–4: Context engineering**
   - Context builder.
   - Context budgets.
   - Session compaction.
   - Artifact references.
   - Persistent memory and retrieval.

     Deliverable: Context engine
3. **Weeks 5–6: Durable execution**
   - Queue-based execution.
   - Checkpointing.
   - Retry and recovery.
   - Long-running task support.
   - Human approval and resume.

     Deliverable: Durable agent execution
4. **Week 7: Enterprise integrations**
   - MCP gateway.
   - A2A integration.
   - Authentication and authorization.
   - Agent registry.

     Deliverable: Interoperability layer
5. **Week 8: Production readiness**
   - OpenTelemetry.
   - Evaluation framework.
   - Load and failure testing.
   - Deployment and dashboards.

     Deliverable: Production release

### **Acceptance tests before production**

Do not consider the harness production-ready until it passes these scenarios:

1. Kill a worker halfway through a 100-task execution and verify recovery.
2. Restart the API service and verify that existing runs remain accessible.
3. Execute multiple tasks in parallel without shared-state corruption.
4. Verify context compaction preserves important task decisions.
5. Resume a task after a human approval delay.
6. Deliver the same queue message twice and verify idempotency.
7. Simulate MCP and A2A timeouts.
8. Verify that an unauthorized agent cannot invoke restricted tools.
9. Compare token consumption before and after context optimization.
10. Reconstruct a complete execution trace from the original request to the final artifact.

## **11. Important implementation references**

There is one particularly relevant Google project I would study before starting from scratch.

**Google ADK Recipes — Long-Horizon Harness**

Highly relevant

[Build Long-running AI agents that pause, resume, and never lose context with ADK                                       - Google Developers Blog](https://images.openai.com/static-rsc-4/GZ-_hPfQ1s_GRzQteL4HH5gy_D55WhzLa0TzjoHvUwwAgp9VoxDUwWcIJJC5X1Fy8vz_bK8_E1IJxRFl_EJLiDIcVUF1Rda9YA0XT06nrUqfscSUQnlqkF4pDbHdahbttblRS8sxtDUi_AmEmlzwDxRwC_GEWUtp_5x-G744KVM?purpose=inline)

[developers.googleblog.com](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/?utm_source=chatgpt.com)

Google's long-horizon harness reference architecture separates the ADK runtime, managed infrastructure and additional harness-level capabilities. It is particularly relevant to your context-management and recovery requirements.

Reference implementation, not a production certification.

[Explore Google Long-Horizon Harness](https://github.com/google/adk-recipes/tree/main/core/python/long-horizon-harness?utm_source=chatgpt.com)

Other useful documentation:

- [ADK App, compaction and resumability configuration](https://github.com/google/adk-python/blob/main/docs/guides/apps/app/index.md?utm_source=chatgpt.com)
- [ADK Context architecture](https://github.com/google/adk-python/blob/main/docs/guides/agents/context/index.md?utm_source=chatgpt.com)
- [ADK Session and persistent state](https://github.com/google/adk-python/blob/main/docs/guides/sessions/session/index.md?utm_source=chatgpt.com)
- [ADK Python developer guides — MCP, A2A, plugins, evaluation and artifacts](https://github.com/google/adk-python/blob/main/docs/guides/README.md?utm_source=chatgpt.com)
- [Google's long-running agent implementation tutorial](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/?utm_source=chatgpt.com)

**Version-specific correction for the earlier code:** In the current ADK guide, `EventsCompactionConfig` is imported from `google.adk.apps.app`, while `App` and `ResumabilityConfig` are available from `google.adk.apps`. Use the current `App` configuration rather than the older `Runner(plugins=...)` pattern.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



# **12. Final architectural recommendation**

I would build this as a reusable platform with the following responsibility boundaries:

| Layer                         | Ownership                                             |
| ----------------------------- | ----------------------------------------------------- |
| Google ADK                    | Agent runtime and execution                           |
| Enterprise Deep Agent Harness | Planning, context, delegation, lifecycle and recovery |
| MCP                           | Tools and resources                                   |
| A2A                           | Agent interoperability                                |
| PostgreSQL                    | Durable task and business execution state             |
| Cloud Storage                 | Workspace and artifacts                               |
| OpenTelemetry                 | Observability                                         |
| Google Cloud                  | Infrastructure and security                           |

# **The architecture I would build**

# **ADK + Deep Agent Harness + MCP + A2A**

**Not another agent framework. An enterprise agent execution platform.**

Your differentiator should be:

- Context-aware execution.
- Long-running autonomous workflows.
- Durable multi-agent collaboration.
- Recoverable task execution.
- Production-grade observability.

One final distinction: this is a proposed reference architecture. ADK provides many underlying primitives, but your task ledger, context policy, recovery orchestration and governance layers are your own engineering responsibilities.

**My strongest recommendation:** Build the context engine and durable execution layer first. Those two capabilities will make a much bigger difference to enterprise reliability than adding more specialized agents.
