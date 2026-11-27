# agent-harness

# AI Agent Harnesses, Agent Products, and Multi-Agent Systems

## A deep-dive field guide based on the AI agent harness model

> **Research snapshot:** November 26, 2026\
> **Primary reading:** [What is an AI agent harness? The body around the
> brain](https://paulshan.com/engineering/what-is-an-ai-agent-harness/)
> by Prasenjit Paul (September 18, 2026)\
> **Companion reading:** [ChatGPT, Claude, Gemini, Grok: the map of what
> each AI company
> sells](https://paulshan.com/engineering/ai-product-map/) (October 6,
> 2026)

This README explains the difference between foundation models, chat
assistants, coding agents, always-on agents, agent platforms, and the
**harness** that makes an AI system capable of doing useful work. It
then maps the major vendor ecosystems and connects the concepts to
production engineering: MCP, A2A, orchestration, memory, computer use,
security, observability, and evaluation.

The goal is not to rank products by hype. It is to give engineers a
durable framework for understanding what each product actually is, what
layer it occupies, and what to evaluate before adopting or building it.

------------------------------------------------------------------------

## Table of contents

1.  [Executive summary](#1-executive-summary)
2.  [The central idea: model + harness =
    agent](#2-the-central-idea-model--harness--agent)
3.  [The five product layers](#3-the-five-product-layers)
4.  [Major AI ecosystems and product
    names](#4-major-ai-ecosystems-and-product-names)
5.  [What an agent harness contains](#5-what-an-agent-harness-contains)
6.  [The agent execution loop](#6-the-agent-execution-loop)
7.  [Harness vs framework vs runtime vs
    orchestrator](#7-harness-vs-framework-vs-runtime-vs-orchestrator)
8.  [MCP and A2A: tools versus
    agents](#8-mcp-and-a2a-tools-versus-agents)
9.  [Single-agent and multi-agent
    architectures](#9-single-agent-and-multi-agent-architectures)
10. [Reference production
    architecture](#10-reference-production-architecture)
11. [Security, governance, and
    reliability](#11-security-governance-and-reliability)
12. [Observability and evaluation](#12-observability-and-evaluation)
13. [How to compare agent products](#13-how-to-compare-agent-products)
14. [Build-versus-buy decision
    framework](#14-build-versus-buy-decision-framework)
15. [Hands-on learning roadmap](#15-hands-on-learning-roadmap)
16. [Glossary](#16-glossary)
17. [Further reading and references](#17-further-reading-and-references)

------------------------------------------------------------------------

## 1. Executive summary

The most important distinction in modern AI engineering is:

**A model is not an agent. An agent is a model operating inside a
software system that gives it context, tools, state, an execution loop,
and constraints.**

A useful shorthand is:

``` text
Agent = Model + Harness
```

The model supplies language understanding, reasoning, and action
proposals. The harness supplies the machinery that turns those proposals
into controlled execution:

-   Context selection: what the model is allowed to see.
-   Tools: what the model is allowed to do.
-   Execution loop: how actions are called, observed, and repeated.
-   State and memory: what persists during and between tasks.
-   Permissions and policy: what is allowed, denied, or requires
    approval.
-   Runtime and sandbox: where code and actions execute.
-   Verification: how the system decides whether the task is actually
    complete.
-   Observability: how engineers reconstruct what happened.
-   Evaluation: how teams measure quality, cost, latency, and safety.

A second important distinction is that vendors sell several different
kinds of products. A model, a chat application, a coding harness, an
autonomous desktop agent, and a developer platform are not
interchangeable categories.

  -----------------------------------------------------------------------
  Layer                   What it is              Main question
  ----------------------- ----------------------- -----------------------
  Model                   The underlying          Which model reasons or
                          foundation model        generates?

  Chat assistant          Conversational product  Where do I talk to it?
                          around a model          

  Coding harness          Model equipped for      What can work on my
                          repository-level work   code?

  Always-on / computer    Agent with a persistent What can work while I
  agent                   environment and a goal  am away?

  Developer platform      APIs, SDKs, hosted      What can I build and
                          runtimes, and           operate?
                          infrastructure          
  -----------------------------------------------------------------------

**Engineering takeaway:** model capability matters, but the harness
determines how that capability is applied, constrained, verified, and
improved in a real workflow.

------------------------------------------------------------------------

## 2. The central idea: model + harness = agent

### 2.1 The model is the brain

A foundation model receives an input and produces an output. In a
typical API interaction, the model does not independently:

-   Browse a website.
-   Read a local repository.
-   Execute a shell command.
-   Query a company database.
-   Send an email.
-   Remember an earlier session unless state is supplied.
-   Verify that an action succeeded in the external world.

The model can propose an action or generate a tool call, but another
piece of software must validate and execute it.

### 2.2 The harness is the body

The harness is the software surrounding the model call. It decides:

-   Which instructions and context are assembled.
-   Which tools are advertised to the model.
-   Whether a proposed action is valid and authorized.
-   How a tool is executed.
-   How tool output is returned to the model.
-   Whether the agent should continue, stop, retry, or ask a human.
-   What state is saved for later.
-   What evidence is retained for debugging and audit.

The harness can use one model or route between several models. It can
also be upgraded without retraining the model.

### 2.3 The agent is the running system

A model plus a harness, executing a task in an environment, is an agent.

``` mermaid
flowchart LR
    U[User goal] --> H[Agent harness]
    H <--> M[Foundation model]
    H <--> T[Tools and APIs]
    H <--> C[Context and retrieval]
    H <--> S[State and memory]
    H <--> P[Policy and approvals]
    H <--> E[Execution environment]
    H --> V[Verification]
    V -->|complete| R[Result]
    V -->|not complete| H
```

### 2.4 Why the same model can produce different outcomes

Imagine two products using the same model to fix a software defect.

-   Product A loads relevant files, runs the failing test, reads the
    stack trace, edits the implementation, reruns tests, and stops only
    when a verifier passes.
-   Product B sends a short prompt and asks the model to suggest a
    patch, but does not run the code.

The difference is not necessarily model intelligence. Product A has a
stronger task-specific harness: repository context, shell access,
iterative execution, and verification.

The same pattern appears outside software engineering. A
customer-support agent with authenticated CRM tools, policy checks, and
approval workflows can do more than a chat window that only explains
what a support employee should do.

### 2.5 Where engineering leverage compounds

Model providers continuously improve model capability. Application teams
can independently improve their harness by adding:

-   Better retrieval and context selection.
-   More precise tool schemas.
-   Safer permissions.
-   Stronger task decomposition.
-   Durable state.
-   Better recovery logic.
-   Deterministic verification.
-   High-quality traces and evaluation datasets.

This creates a useful strategic separation:

-   **Rent or select the model capability.**
-   **Own the workflow, policies, integrations, evaluations, and
    domain-specific harness.**

That does not mean every company should build a complete agent platform.
It means the harness is a first-class engineering asset and should be
designed deliberately.

------------------------------------------------------------------------

## 3. The five product layers

The product-map article provides a useful taxonomy: one model layer and
four product layers built around it.

### 3.1 Layer 1 --- Foundation models

The model is the reasoning and generation engine. It may be proprietary
and accessed through an API, or open-weight and deployed by the user.

Examples of model families include:

-   OpenAI GPT models.
-   Anthropic Claude models.
-   Google Gemini models.
-   xAI Grok models.
-   Meta Llama models.
-   DeepSeek models.
-   Alibaba Qwen models.
-   Mistral models.
-   Other open-weight and commercial models.

A model comparison should consider more than benchmark scores:

-   Reasoning quality on the target workload.
-   Tool-call accuracy and schema adherence.
-   Long-context behavior.
-   Multimodal input/output requirements.
-   Latency and throughput.
-   Token and infrastructure cost.
-   Data handling and deployment constraints.
-   Reliability across repeated runs.

### 3.2 Layer 2 --- Chat assistants

A chat assistant packages a model with a conversational interface and
product features such as history, file upload, voice, search, memory,
and integrations.

Examples:

-   ChatGPT.
-   Claude.
-   Google Gemini.
-   Grok.
-   Microsoft Copilot.
-   Perplexity.
-   Meta AI.
-   DeepSeek Chat.
-   Le Chat.
-   Qwen Chat.
-   Amazon Q experiences.
-   ERNIE Bot.

A chat assistant is not automatically an autonomous agent. A chat
product may provide agentic capabilities, but a conventional
question-and-answer interaction is not the same as a system that
executes a multi-step task and verifies the result.

### 3.3 Layer 3 --- Coding harnesses

A coding harness gives a model a software-development environment,
usually including:

-   Repository and file access.
-   Search and navigation.
-   File editing and patch application.
-   Terminal or shell execution.
-   Build and test commands.
-   Git or version-control workflows.
-   Context management.
-   Approval controls.
-   Sandboxing.
-   Iterative verification.

Examples in the current ecosystem include:

-   OpenAI Codex.
-   Anthropic Claude Code.
-   Google Antigravity and Gemini CLI.
-   Cursor.
-   Cline.
-   Aider.
-   OpenCode.
-   OpenHands.
-   Goose.
-   Pi.

These products differ in IDE integration, terminal-first workflows,
supported models, autonomy, cloud execution, review experience, and
extensibility. Do not assume every product supports every capability or
model provider.

### 3.4 Layer 4 --- Always-on and computer-use agents

These systems accept a goal and may continue working in a persistent or
hosted environment. Some provide a cloud computer, browser, terminal,
filesystem, or application integrations.

The October 2026 product-map article identifies the following vendor
names in this category:

-   OpenAI: dots.
-   Anthropic: Claude Cowork.
-   Google: Gemini Spark.
-   Meta: Muse.
-   xAI: Grok Bot.
-   Open-source / self-hosted examples: OpenClaw and Hermes Agent.

These are product names and category placements reported in the cited
October 2026 market map. Product scope, preview/GA status, regional
availability, and naming can change. Verify current vendor documentation
before making purchasing or architecture decisions.

Computer-use agents deserve special attention because they operate
through interfaces designed for humans. They may click, type, navigate,
and inspect screen state. This is powerful but can be more fragile than
a typed API: layout changes, latency, pop-ups, ambiguous buttons, and
unexpected page state can all cause errors.

### 3.5 Layer 5 --- Developer platforms

Developer platforms expose models and/or agent execution capabilities
through APIs, SDKs, managed runtimes, and infrastructure.

Examples include:

-   OpenAI API, Responses API, Agents SDK, and Agents API.
-   Anthropic API, Claude Agent SDK, and managed agent capabilities.
-   Google Gemini API, Vertex AI, Agent Development Kit (ADK), and
    related tooling.
-   xAI API.
-   Meta model offerings and Llama ecosystem.
-   Open-source serving and orchestration stacks such as vLLM, Ollama,
    LangGraph, and related tools.

The crucial platform question is whether the provider rents only the
model, or also manages part of the harness: sessions, tools, sandbox,
context compaction, retries, handoffs, and recovery.

------------------------------------------------------------------------

## 4. Major AI ecosystems and product names

This section separates **models**, **chat products**, **coding
harnesses**, **always-on agents**, and **developer platforms**. Names
below are an ecosystem map, not a claim that every feature is available
to every user or in every region.

### 4.1 Vendor comparison

  ---------------------------------------------------------------------------------------
  Ecosystem    Model family  Chat         Coding /       Always-on /         Builder
                             assistant    developer      computer agent      platform
                                          harness                            
  ------------ ------------- ------------ -------------- ------------------- ------------
  OpenAI       GPT           ChatGPT      Codex          dots                OpenAI API,
                                                                             Responses
                                                                             API, Agents
                                                                             SDK / Agents
                                                                             API

  Anthropic    Claude        Claude       Claude Code    Claude Cowork       Claude API /
                                                                             Agent SDK /
                                                                             managed
                                                                             agent
                                                                             offerings

  Google       Gemini        Gemini       Antigravity,   Gemini Spark        Gemini API,
                                          Gemini CLI                         Vertex AI,
                                                                             ADK

  xAI          Grok          Grok         Grok Build (as Grok Bot            xAI API
                                          listed in the                      
                                          market map)                        

  Meta         Llama; Muse   Meta AI      Muse Code (as  Muse                Meta model
               family in the              listed in the                      ecosystem /
               cited map                  market map)                        Llama
                                                                             weights

  Microsoft    Models from   Microsoft    GitHub Copilot Copilot agent       Azure AI
               multiple      Copilot      coding agent   experiences         Foundry and
               providers                  and related                        Microsoft
               plus                       tools                              agent
               Microsoft                                                     tooling
               models                                                        

  Perplexity   Multi-model   Perplexity   Product        Comet /             Perplexity
               product                    capabilities   computer-oriented   API and
               approach                   evolve; verify experiences         enterprise
                                          current                            offerings
                                          offerings                          

  DeepSeek     DeepSeek      DeepSeek     Coding         No single universal DeepSeek API
                             Chat         integrations   always-on product   / open model
                                          and            assumed here        ecosystem
                                          third-party                        
                                          harnesses                          

  Mistral      Mistral       Le Chat      Mistral Vibe   Verify current      Mistral AI
               models                     and            product status      platform
                                          integrations                       

  Alibaba      Qwen          Qwen Chat    Qwen coding    Varies by product   Model Studio
                                          tools and                          / Qwen
                                          third-party                        ecosystem
                                          harnesses                          

  Open source  Llama, Qwen,  Open WebUI,  OpenCode, Pi,  OpenClaw, Hermes    Ollama,
               DeepSeek,     LibreChat    Aider, Cline,  Agent               vLLM,
               Mistral, Kimi              OpenHands,                         LangGraph
               and others                 Goose                              and other
                                                                             runtimes
  ---------------------------------------------------------------------------------------

**Important naming correction:** "Claude Duet" and "Gemini Task" should
not be treated as established product names based on the cited market
map. The October 2026 map uses **Claude Cowork** and **Gemini Spark**
for the always-on-agent row. Similarly, do not use generic labels such
as "Grok Bot" as if they were the underlying Grok model; they refer to a
product category/name in that market map.

### 4.2 OpenAI

  -----------------------------------------------------------------------
  Category                Name                    What it represents
  ----------------------- ----------------------- -----------------------
  Model                   GPT model family        Foundation models

  Chat                    ChatGPT                 General conversational
                                                  assistant

  Coding harness          Codex                   Software engineering
                                                  agent and coding
                                                  workflow

  Always-on agent         dots                    Personal agent product
                                                  identified in the
                                                  October 2026 market map

  Builder interfaces      Responses API           Lower-level model and
                                                  tool interaction

  Agent framework         Agents SDK              Code-first
                                                  orchestration, tools,
                                                  handoffs, guardrails,
                                                  tracing

  Managed agent runtime   Agents API              Hosted Codex harness,
                                                  sessions, context
                                                  management, sandbox
                                                  options
  -----------------------------------------------------------------------

**Engineering interpretation:** OpenAI offers both a route where the
developer owns more of the loop and a managed route where the platform
runs more of the harness. The correct choice depends on control,
deployment, state, compliance, and operational requirements.

### 4.3 Anthropic

  ------------------------------------------------------------------------------
  Category                Name                    What it represents
  ----------------------- ----------------------- ------------------------------
  Model                   Claude model family     Foundation models

  Chat                    Claude                  Conversational assistant

  Coding harness          Claude Code             Terminal/repository-oriented
                                                  coding agent

  General work agent      Claude Cowork           Agentic work product
                                                  identified in the October 2026
                                                  map

  Builder interfaces      Claude API              Model and tool integration

  Agent development       Claude Agent SDK /      Build or host agent workflows
                          managed offerings       
  ------------------------------------------------------------------------------

**Engineering interpretation:** Claude Code is a useful example for
studying a coding harness: repository context, tool use, command
execution, permissions, and iterative work are central to its value.
Cowork belongs to a different product category; do not compare it
directly with a model API.

### 4.4 Google

  -----------------------------------------------------------------------
  Category                Name                    What it represents
  ----------------------- ----------------------- -----------------------
  Model                   Gemini family           Foundation models

  Chat                    Gemini app              Conversational
                                                  assistant

  Coding harness          Antigravity, Gemini CLI Coding and
                                                  agent-development
                                                  environments

  Always-on agent         Gemini Spark            Name used in the
                                                  October 2026 product
                                                  map

  Builder platform        Gemini API, Vertex AI   Model access and
                                                  enterprise
                                                  infrastructure

  Agent framework         Agent Development Kit   Build and orchestrate
                          (ADK)                   agents
  -----------------------------------------------------------------------

**Engineering interpretation:** Google's ecosystem spans consumer
assistants, coding environments, cloud infrastructure, and
agent-development frameworks. ADK is a framework for building agents; it
is not itself a foundation model.

### 4.5 xAI

  -----------------------------------------------------------------------
  Category                Name                    What it represents
  ----------------------- ----------------------- -----------------------
  Model                   Grok family             Foundation models

  Chat                    Grok                    Conversational
                                                  assistant

  Coding harness          Grok Build              Name used in the
                                                  October 2026 product
                                                  map

  Always-on agent         Grok Bot                Name used in the
                                                  October 2026 product
                                                  map

  Builder platform        xAI API                 Model access and
                                                  integrations
  -----------------------------------------------------------------------

**Engineering interpretation:** Keep the Grok model, Grok chat product,
and agent/coding products conceptually separate. Check current xAI
documentation for supported APIs and product status.

### 4.6 Meta

  -----------------------------------------------------------------------
  Category                Name                    What it represents
  ----------------------- ----------------------- -----------------------
  Models                  Llama; Muse family in   Model ecosystem
                          the cited map           

  Chat                    Meta AI                 Consumer assistant

  Coding harness          Muse Code               Name used in the
                                                  October 2026 product
                                                  map

  Always-on agent         Muse                    Name used in the
                                                  October 2026 product
                                                  map

  Builder platform        Meta model ecosystem /  Model access and
                          Llama weights           deployment choices
  -----------------------------------------------------------------------

**Engineering interpretation:** Meta has both open-weight model
offerings and newer product names in the cited market map. Open weights
can provide deployment flexibility, but the organization takes on
hosting, scaling, security, and model lifecycle responsibilities.

### 4.7 Open-source and model-agnostic ecosystem

  Project        Main role
  -------------- -------------------------------------------------------
  Open WebUI     Self-hosted chat interface for model providers
  LibreChat      Multi-provider conversational interface
  OpenCode       Model-agnostic coding harness
  Pi             Minimal agent/coding harness and extensible toolkit
  Aider          Git-aware AI pair-programming tool
  Cline          IDE-based coding agent
  OpenHands      Software engineering agent platform
  Goose          Extensible open-source agent
  OpenClaw       Personal-agent project
  Hermes Agent   Agent system with persistent and extensible workflows
  Ollama         Run supported models locally
  vLLM           High-throughput model serving
  LangGraph      Stateful agent workflow/orchestration framework

Open source is not one product. It is a collection of interchangeable
model servers, interfaces, harnesses, frameworks, and integrations. This
modularity is valuable when you need model portability or control over
deployment.

------------------------------------------------------------------------

## 5. What an agent harness contains

A production harness is more than a prompt and a `while` loop. The
following components form a practical design checklist.

### 5.1 Task intake and specification

Convert a vague request into an explicit task contract:

-   Objective and expected output.
-   Scope and exclusions.
-   Available data and tools.
-   Success criteria.
-   Deadline, cost, and iteration limits.
-   Approval requirements.
-   Required evidence or artifacts.

A task should be testable. "Improve the service" is ambiguous;
"reproduce issue 481, implement a fix, run the unit and integration
suites, and provide a patch plus test evidence" is much more actionable.

### 5.2 Context engineering

Context engineering decides what information enters each model call.

Common context sources:

-   User request and conversation state.
-   System and developer instructions.
-   Repository files and documentation.
-   Search results and retrieved records.
-   Tool descriptions and schemas.
-   Prior tool outputs.
-   Project-specific rules and skills.
-   Relevant long-term memory.

Good context is selected, ranked, scoped, and refreshed. Sending every
available document to the model is usually wasteful and may reduce
accuracy.

### 5.3 Tool registry and tool contracts

Tools are the agent's action surface. Examples:

-   Search documents.
-   Read a file.
-   Query a database.
-   Open a pull request.
-   Execute a command.
-   Send a notification.
-   Create a ticket.
-   Navigate a browser.

A good tool contract has:

-   A precise name and description.
-   Typed input schema.
-   Typed output schema.
-   Authentication and authorization rules.
-   Timeout and retry policy.
-   Idempotency behavior.
-   Error semantics.
-   Audit metadata.

Prefer narrow, task-oriented tools over giant tools with ambiguous
behavior. A `get_customer_invoice(invoice_id)` tool is easier to reason
about than a generic `execute_any_database_query(sql)` tool.

### 5.4 Orchestration loop

The loop coordinates model calls, tool execution, observations, retries,
and stopping. It should be deterministic where possible and bounded by
explicit limits.

### 5.5 State and memory

Distinguish three kinds of state:

1.  **Turn state:** messages, tool calls, and results for the current
    interaction.
2.  **Task/session state:** progress, intermediate artifacts,
    checkpoints, and pending approvals.
3.  **Long-term memory:** durable facts, preferences, project
    conventions, and lessons that may help future tasks.

Do not treat raw conversation history as a complete memory architecture.
Long-term memory needs provenance, freshness, access controls, retention
rules, and correction mechanisms.

### 5.6 Runtime and environment

The runtime determines where actions happen:

-   Local process.
-   Container.
-   Kubernetes job or pod.
-   Hosted sandbox.
-   Remote desktop or browser.
-   Cloud VM.
-   Enterprise application environment.

The environment should be isolated from unrelated workloads and
production credentials. Use ephemeral workspaces when possible.

### 5.7 Permissions and human approvals

The harness should make the authority boundary explicit:

-   Read-only access.
-   Draft-only access.
-   Write access to a scoped workspace.
-   External communication.
-   Financial or irreversible actions.
-   Production changes.

For high-impact actions, use a proposal/approval/execute pattern. The
model should not be able to grant itself more authority.

### 5.8 Verification and stopping conditions

The model saying "done" is not proof of completion.

Use independent checks such as:

-   Unit and integration tests.
-   Schema validation.
-   Static analysis.
-   Policy checks.
-   Database invariants.
-   Artifact existence and content checks.
-   Human review.
-   External system confirmation.

Define explicit stop conditions: success, maximum steps, timeout, budget
exhausted, repeated failure, missing permission, or human intervention
required.

### 5.9 Observability

Capture enough structured information to answer:

-   What did the user ask?
-   Which model and prompt version were used?
-   What context was supplied?
-   Which tools were available?
-   Which tools were called, with what arguments?
-   What did they return?
-   Which policies were evaluated?
-   How many retries occurred?
-   What did verification prove?
-   What did the task cost and how long did it take?

Protect logs from secrets and sensitive payloads. Observability is not a
reason to retain everything forever.

------------------------------------------------------------------------

## 6. The agent execution loop

A simple ReAct-style loop alternates between reasoning, action, and
observation. The exact implementation varies by framework and model API.

``` mermaid
flowchart TD
    A[Receive task] --> B[Validate task and identity]
    B --> C[Build context and tool set]
    C --> D[Call model]
    D --> E{Final response or tool request?}
    E -->|Tool request| F[Validate schema and policy]
    F --> G{Approval required?}
    G -->|Yes| H[Request human approval]
    H -->|Approved| I[Execute in controlled runtime]
    H -->|Denied| J[Return denial to agent]
    G -->|No| I
    I --> K[Capture tool result]
    K --> L[Update state and trace]
    L --> M{Budget / step limit exceeded?}
    M -->|No| C
    M -->|Yes| N[Stop safely]
    J --> C
    E -->|Final| O[Run completion verifier]
    O --> P{Verified?}
    P -->|Yes| Q[Return result and evidence]
    P -->|No| C
```

### 6.1 Conceptual pseudocode

``` python
async def run_agent(task, session, policy, tools, model):
    state = await session.load_or_create(task)
    trace = start_trace(task, state)

    for step in range(policy.max_steps):
        context = await build_context(
            task=task,
            state=state,
            tool_catalog=tools.allowed_for(policy),
            token_budget=policy.context_budget,
        )

        response = await model.respond(context)

        if response.is_final:
            verdict = await verify_completion(task, response, state)

            if verdict.passed:
                await session.save(state)
                trace.finish(status="verified_success")
                return response, verdict.evidence

            state.add_verification_failure(verdict)
            continue

        for call in response.tool_calls:
            args = validate_schema(call.arguments, call.schema)
            decision = await policy.authorize(
                identity=session.identity,
                tool=call.name,
                arguments=args,
            )

            if decision.requires_approval:
                decision = await request_human_approval(decision)

            if not decision.allowed:
                state.add_tool_denial(call, decision.reason)
                continue

            result = await tools.execute(
                call.name,
                args,
                sandbox=session.sandbox,
                timeout=policy.tool_timeout,
            )
            state.add_observation(call, result)
            trace.record_tool(call, result)

        await session.checkpoint(state)

    trace.finish(status="limit_reached")
    return safe_incomplete_result(state)
```

This is illustrative pseudocode, not a drop-in implementation.
Production systems also need cancellation, concurrency control, retries
with backoff, idempotency, structured error handling, secrets
management, and durable recovery.

### 6.2 ReAct, planning, and workflow patterns

  -----------------------------------------------------------------------
  Pattern                 Description             Best fit
  ----------------------- ----------------------- -----------------------
  ReAct                   Interleave reasoning    Dynamic tasks where the
                          and tool actions        next action depends on
                                                  observations

  Plan-and-execute        Create a plan, then     Tasks with
                          execute steps           understandable phases

  Workflow / state        Explicit transitions    Regulated or repeatable
  machine                 and deterministic       business processes
                          control                 

  Router                  Select a specialist or  Multi-domain systems
                          tool based on intent    

  Supervisor / workers    A coordinator delegates Parallelizable work
                          to specialist agents    with clear boundaries

  Event-driven            Continue from events,   Long-running
                          queues, or callbacks    asynchronous tasks
  -----------------------------------------------------------------------

Do not use free-form autonomous planning when a deterministic workflow
is safer, cheaper, and easier to test.

------------------------------------------------------------------------

## 7. Harness vs framework vs runtime vs orchestrator

These terms overlap in industry discussions. Define them explicitly in
architecture documents.

  -----------------------------------------------------------------------
  Term                    Meaning                 Example / analogy
  ----------------------- ----------------------- -----------------------
  Model                   Neural network that     Brain
                          generates outputs and   
                          action proposals        

  Agent                   Model plus harness,     Worker in action
                          running toward a goal   

  Harness                 Application-level       Body and operating
                          control system around   procedures
                          model calls             

  Framework / SDK         Reusable library for    Toolkit
                          building agents and     
                          harnesses               

  Runtime                 Environment that        Operating environment
                          executes code, tools,   
                          sessions, and workloads 

  Orchestrator            Component coordinating  Scheduler / conductor
                          steps, agents, and      
                          dependencies            

  Wrapper                 Thin layer around a     Basic adapter
                          model call, often       
                          without a robust loop   

  Prompt engineering      Improving instructions  Instruction design
                          supplied to a model     

  Context engineering     Selecting and managing  Information
                          the information         architecture
                          supplied to the model   

  Evaluation harness      Test runner and scoring QA lab
                          environment for         
                          model/agent behavior    
  -----------------------------------------------------------------------

Examples of frameworks and SDKs include LangGraph, OpenAI Agents SDK,
Anthropic Agent SDK, Google ADK, and other agent-development libraries.
These provide building blocks; a production application still has to
define its domain policies, tools, deployment, data boundaries, and
success criteria.

------------------------------------------------------------------------

## 8. MCP and A2A: tools versus agents

MCP and A2A solve related but different interoperability problems.

### 8.1 MCP --- Model Context Protocol

MCP standardizes how an AI application connects to external tools and
context providers.

A simplified relationship:

``` text
Agent / MCP host
    |
    +-- MCP client ---- MCP server: database tools
    |
    +-- MCP client ---- MCP server: document search
    |
    +-- MCP client ---- MCP server: ticketing system
    |
    +-- MCP client ---- MCP server: internal APIs
```

MCP is useful when you want a consistent way to expose capabilities such
as:

-   Tools: executable operations.
-   Resources: contextual data exposed by a server.
-   Prompts: reusable prompt templates or workflows.
-   Other protocol features supported by the applicable specification
    version.

MCP does not decide your entire agent architecture. Your harness still
owns task planning, authorization, execution policy, memory,
verification, and user experience.

**Security note:** an MCP server is a capability boundary. Treat each
server and each tool as an integration with explicit trust, identity,
authorization, input validation, and audit requirements.

Official documentation: https://modelcontextprotocol.io/

### 8.2 A2A --- Agent2Agent Protocol

A2A is designed for communication and collaboration between independent
agents, including agents built with different frameworks or by different
vendors.

A simplified relationship:

``` text
Client / coordinator agent
       |
       +---- A2A ---- Research agent
       |
       +---- A2A ---- Data analysis agent
       |
       +---- A2A ---- Enterprise workflow agent
```

A2A helps with agent discovery and interoperable task collaboration. It
is not a replacement for an agent framework and is not the protocol for
an agent's ordinary tool calls.

Official documentation: https://a2a-protocol.org/

### 8.3 MCP vs A2A

  -----------------------------------------------------------------------
  Dimension               MCP                     A2A
  ----------------------- ----------------------- -----------------------
  Primary purpose         Connect an AI           Connect independent
                          application to tools    agents
                          and context             

  Communication           Agent/application ↔     Agent ↔ agent
  relationship            tool or context server  

  Typical use             Search a document       Delegate a research or
                          store, query a service, analysis task to
                          create a ticket         another agent

  Does it define the      No                      No
  agent's reasoning loop?                         

  Does it replace a       No                      No
  framework?                                      

  Typical complement      Agent framework + MCP   Agent framework + A2A
                          servers                 peers
  -----------------------------------------------------------------------

**Rule of thumb:** use MCP to give an agent tools; use A2A when one
agent needs to collaborate with another independent agent.

### 8.4 Combining MCP and A2A

``` mermaid
flowchart TD
    U[User] --> C[Coordinator agent]
    C -->|MCP| D[Document search tools]
    C -->|MCP| DB[Database tools]
    C -->|A2A| R[Research agent]
    C -->|A2A| A[Analytics agent]
    R -->|MCP| W[Web / knowledge tools]
    A -->|MCP| Q[Warehouse tools]
    R --> C
    A --> C
    C --> V[Verify and synthesize]
    V --> U
```

This separates the integration layer from the collaboration layer. Each
agent can own its own model, harness, tools, and policy boundary.

------------------------------------------------------------------------

## 9. Single-agent and multi-agent architectures

Multi-agent systems are not automatically better. They add coordination
overhead, more model calls, more state, more failure modes, and a larger
security surface. Start with one well-designed agent unless independent
roles or parallelism justify multiple agents.

### 9.1 Single agent

``` text
User -> Agent -> Tools -> Verification -> Result
```

Advantages: - Simpler state and debugging. - Lower coordination
overhead. - Easier authorization model. - Often lower latency and cost.

Limitations: - One context can become overloaded. - Specialist behavior
may be difficult to isolate. - Some tasks cannot be parallelized
efficiently.

### 9.2 Supervisor and specialist agents

``` text
                 Supervisor
                /    |     \
          Research  Data   Compliance
             |       |        |
           Tools    Tools    Policies
                \    |     /
                Synthesizer
                     |
                  Verifier
```

The supervisor decomposes work, assigns tasks, gathers results, resolves
conflicts, and produces the final output.

Use this pattern when: - Subtasks are separable. - Different roles need
different tools or permissions. - Parallel execution improves elapsed
time. - Independent review adds value.

Avoid it when the task is small, the agents share the same context, or
the supervisor cannot reliably verify the workers.

### 9.3 Common multi-agent patterns

  -----------------------------------------------------------------------
  Pattern                 Description             Risk to manage
  ----------------------- ----------------------- -----------------------
  Supervisor-worker       One agent delegates to  Supervisor bottleneck
                          specialists             and poor delegation

  Sequential pipeline     Output of one agent     Error propagation
                          becomes input to        
                          another                 

  Parallel fan-out/fan-in Several agents work     Conflicts and
                          independently; results  duplicated work
                          are merged              

  Debate / critique       Agents challenge or     Cost and false
                          review a proposal       consensus

  Blackboard              Agents contribute to    Race conditions and
                          shared state            stale state

  Hierarchical            Supervisors manage      Complex failure
                          sub-supervisors and     attribution
                          workers                 

  Event-driven agents     Agents react to events  Duplicate events and
                          and publish results     eventual consistency
  -----------------------------------------------------------------------

### 9.4 Agent handoff contract

Every delegated task should carry a structured contract:

``` json
{
  "task_id": "task-123",
  "objective": "Analyze service latency regression",
  "scope": ["service-a", "deployment-2026-11-20"],
  "constraints": ["read-only", "no production changes"],
  "expected_output": {
    "format": "json",
    "fields": ["findings", "evidence", "confidence", "recommended_actions"]
  },
  "deadline_seconds": 180,
  "correlation_id": "trace-abc"
}
```

A handoff should define ownership, input references, expected output,
deadline, permissions, and failure behavior. Do not rely on an
unstructured paragraph as the only inter-agent contract.

------------------------------------------------------------------------

## 10. Reference production architecture

A production architecture separates the user-facing layer, agent control
plane, execution plane, integration plane, and governance/observability
plane.

``` mermaid
flowchart TB
    U[User / API client] --> GW[API gateway and identity]
    GW --> ORCH[Agent orchestrator / harness]

    subgraph Control_Plane[Control plane]
      ORCH
      REG[Agent and tool registry]
      POL[Policy engine]
      MEM[Session state and memory]
      CTX[Context builder / retrieval]
      ROUTER[Model router]
    end

    ORCH <--> REG
    ORCH <--> POL
    ORCH <--> MEM
    ORCH <--> CTX
    ORCH <--> ROUTER

    ROUTER --> LLM[Model providers]
    ORCH --> EXEC[Sandbox / browser / computer runtime]

    subgraph Integration_Plane[Integration plane]
      MCP[MCP servers]
      API[Internal APIs]
      DB[Databases and data platforms]
      SAAS[Enterprise SaaS]
      A2A[A2A remote agents]
    end

    EXEC <--> MCP
    ORCH <--> MCP
    ORCH <--> API
    ORCH <--> DB
    ORCH <--> SAAS
    ORCH <--> A2A

    subgraph Assurance_Plane[Assurance plane]
      TRACE[Traces and logs]
      EVAL[Evaluation service]
      AUDIT[Audit records]
      HUMAN[Human approval queue]
    end

    ORCH --> TRACE
    ORCH --> AUDIT
    ORCH <--> HUMAN
    TRACE --> EVAL
    EVAL --> ORCH
```

### 10.1 Suggested service boundaries

  -----------------------------------------------------------------------
  Service                             Responsibility
  ----------------------------------- -----------------------------------
  API gateway                         Authentication, rate limits,
                                      request validation

  Agent orchestrator                  Task lifecycle, loop, delegation,
                                      cancellation

  Model gateway                       Provider abstraction, routing,
                                      fallback, budgets

  Context service                     Retrieval, ranking, summarization,
                                      context budgets

  Tool gateway                        Tool discovery, schema validation,
                                      invocation

  Policy engine                       Authorization, data policy, action
                                      approvals

  Session service                     Durable task state, checkpoints,
                                      resumability

  Sandbox manager                     Isolated execution environments

  Observability service               Traces, metrics, logs, audit
                                      correlation

  Evaluation service                  Offline tests, online quality
                                      checks, regression detection
  -----------------------------------------------------------------------

### 10.2 Model gateway considerations

A model gateway can help with: - Provider selection and failover. -
Model-specific request adaptation. - Rate limits and concurrency. - Cost
accounting. - Prompt and model version tracking. - Retry
classification. - Data residency and provider policy enforcement.

However, abstraction can hide model-specific behavior. Preserve
provider-specific capabilities where they matter, and test every route
with the actual task distribution.

### 10.3 Durable execution

Long-running agents need durable execution rather than relying on one
in-memory process.

Persist: - Task ID and user/tenant identity. - Current state and plan. -
Completed steps and outputs. - Pending tool calls or approvals. - Retry
counters and deadlines. - Correlation and trace IDs. - Artifact
references. - Model and policy versions.

Design for process restarts, worker crashes, duplicated events,
timeouts, and user cancellation.

------------------------------------------------------------------------

## 11. Security, governance, and reliability

An agent harness is also a security boundary. The more tools an agent
can use, the more important it is to constrain the actions it can take.

### 11.1 Least privilege

Grant only the minimum access needed for the task.

-   Prefer read-only tools for investigation.
-   Scope file access to a workspace.
-   Scope database access to approved schemas and queries.
-   Use short-lived credentials.
-   Separate development, staging, and production identities.
-   Avoid passing broad secrets into model context.

### 11.2 Prompt injection and untrusted content

Treat retrieved documents, websites, emails, issue comments, and tool
outputs as untrusted data. They may contain instructions that attempt to
override the agent's task or extract secrets.

Controls: - Keep trusted instructions separate from retrieved content. -
Label untrusted data explicitly. - Do not let retrieved content modify
permissions. - Require policy checks outside the model. - Restrict tools
and data access by task. - Use human review for sensitive actions. -
Test with adversarial prompt-injection cases.

### 11.3 Tool safety

Before execution: 1. Validate the tool name and arguments. 2. Check the
caller's identity and authorization. 3. Apply resource-level policy. 4.
Enforce rate, time, and spend limits. 5. Require approval for sensitive
actions. 6. Execute in a controlled environment. 7. Record the outcome.

### 11.4 Reliability patterns

  -----------------------------------------------------------------------
  Failure                             Recommended control
  ----------------------------------- -----------------------------------
  Tool timeout                        Bounded timeout, retry policy,
                                      cancellation

  Duplicate action                    Idempotency key and deduplication

  Invalid arguments                   Schema validation and typed errors

  Model loop                          Max steps, budget, deadline,
                                      repeated-state detection

  Partial failure                     Checkpoints and resumable task
                                      state

  Wrong final answer                  Independent verifier and evidence

  Provider outage                     Circuit breaker and controlled
                                      fallback

  Unsafe action                       Policy engine and approval gate

  Context overflow                    Context budget, compaction,
                                      retrieval

  Conflicting agent outputs           Evidence-based reconciliation and
                                      explicit ownership
  -----------------------------------------------------------------------

### 11.5 Human-in-the-loop design

Human approval should be part of the workflow, not an afterthought.

A good approval request shows: - The proposed action. - The target
system and affected records. - The reason for the action. - The exact
parameters or diff. - The expected consequence. - Whether the action is
reversible. - Who is requesting approval. - Expiration time and audit
reference.

A human should approve a concrete action, not a vague statement such as
"allow the agent to continue."

------------------------------------------------------------------------

## 12. Observability and evaluation

A production agent should be evaluated as a system, not just as a model
response.

### 12.1 Trace structure

A useful trace hierarchy:

``` text
agent.task
  ├── context.build
  ├── model.call
  ├── tool.authorize
  ├── tool.execute
  ├── model.call
  ├── agent.handoff
  │     └── child_agent.task
  ├── verification.run
  └── agent.complete
```

Each event should carry appropriate correlation identifiers: -
`trace_id` - `task_id` - `session_id` - `tenant_id` (non-sensitive
internal identifier) - `agent_id` - `model_id` - `tool_name` -
`policy_version` - `prompt_version`

Avoid placing secrets or unnecessary personal data in telemetry.

### 12.2 Core metrics

  -----------------------------------------------------------------------
  Category                            Metrics
  ----------------------------------- -----------------------------------
  Quality                             Task success rate, verifier pass
                                      rate, human acceptance

  Reliability                         Tool error rate, retries, timeout
                                      rate, recovery rate

  Efficiency                          Steps per task, tool calls per
                                      task, tokens per task

  Performance                         Time to first action, end-to-end
                                      latency, queue time

  Cost                                Model cost, tool cost, sandbox
                                      cost, total cost per successful
                                      task

  Safety                              Policy denials, approval rate,
                                      unsafe-action test failures

  User experience                     Abandonment, correction rate,
                                      satisfaction, escalation rate
  -----------------------------------------------------------------------

Measure **cost per successful task**, not only cost per model call. A
cheaper model that needs many retries may be more expensive overall.

### 12.3 Evaluation layers

1.  **Unit tests:** tool schemas, policy functions, state transitions.
2.  **Integration tests:** model + tools + runtime behavior.
3.  **Scenario tests:** representative user tasks and edge cases.
4.  **Adversarial tests:** prompt injection, malformed tool output,
    permission escalation.
5.  **Regression tests:** compare new prompts, models, and harness
    versions.
6.  **Online monitoring:** detect drift, latency spikes, and failure
    clusters.
7.  **Human review:** evaluate quality where automated scoring is
    insufficient.

### 12.4 Evidence-based completion

A strong agent response should distinguish: - What it completed. - What
it attempted but could not complete. - What it verified. - What remains
uncertain. - What needs human action.

For coding agents, a successful patch plus passing tests is stronger
evidence than a confident explanation. For enterprise agents, a
confirmed transaction ID or system response is stronger evidence than
"the request has been submitted."

------------------------------------------------------------------------

## 13. How to compare agent products

Compare products within the same category. A model versus a chat app is
not an apples-to-apples comparison; neither is a coding harness versus
an always-on personal agent.

### 13.1 Product evaluation matrix

  -----------------------------------------------------------------------
  Dimension                           Questions to ask
  ----------------------------------- -----------------------------------
  Model choice                        Which models are supported? Can I
                                      bring my own model?

  Tool support                        Native tools, custom functions,
                                      MCP, browser, shell, APIs?

  Context                             How are files, search results, and
                                      long conversations handled?

  Memory                              What persists? Can memory be
                                      inspected, corrected, or deleted?

  Execution                           Local, cloud, container, VM,
                                      browser, or remote computer?

  Autonomy                            Does it propose, draft, execute, or
                                      continue unattended?

  Approvals                           Can I approve individual actions?
                                      Are policies configurable?

  Multi-agent                         Can it delegate? Are handoffs
                                      traceable?

  Reliability                         Retries, checkpoints, resumability,
                                      cancellation?

  Observability                       Are tool calls, model calls, and
                                      decisions traceable?

  Security                            Identity, isolation, secrets, data
                                      retention, audit?

  Portability                         Can I switch models, tools, or
                                      deployment providers?

  Cost                                What is the full cost per completed
                                      task?

  Governance                          Enterprise controls, retention,
                                      residency, compliance support?
  -----------------------------------------------------------------------

### 13.2 Choose by use case

  -----------------------------------------------------------------------
  Use case                            Product category to evaluate first
  ----------------------------------- -----------------------------------
  Ask questions and analyze documents Chat assistant

  Research with citations and web     Research-oriented assistant
  access                              

  Modify a software repository        Coding harness

  Operate websites and desktop        Computer-use / always-on agent
  workflows                           

  Build a custom internal agent       Developer platform + framework

  Connect tools across vendors        MCP

  Delegate work across independent    A2A
  agent systems                       

  Run models on controlled            Open-weight model + serving runtime
  infrastructure                      

  Operate a regulated workflow        Custom harness with explicit policy
                                      and verification
  -----------------------------------------------------------------------

### 13.3 A practical bake-off

Use the same representative task set for every candidate:

-   A straightforward task.
-   A multi-step task with ambiguous requirements.
-   A task requiring several tools.
-   A task with a recoverable tool failure.
-   A task containing prompt injection in retrieved content.
-   A task requiring human approval.
-   A task requiring a verifiable final artifact.

Record success, quality, time, cost, tool-call accuracy, unsafe
behavior, and the amount of human intervention. Repeat each scenario
enough times to account for stochastic variation.

------------------------------------------------------------------------

## 14. Build-versus-buy decision framework

### 14.1 Buy or use a managed harness when

-   The workflow is common and vendor-supported.
-   Time to value is more important than deep control.
-   The provider's security and deployment model meets requirements.
-   Managed sessions, sandboxing, and recovery reduce operational
    burden.
-   You do not need unusual domain-specific execution semantics.

### 14.2 Build your own harness when

-   The workflow is core intellectual property.
-   You need strict control over tools, data, and permissions.
-   The environment is specialized.
-   You need deterministic business processes around model decisions.
-   You need multi-provider routing or model portability.
-   You require custom audit, retention, and verification behavior.
-   Existing products cannot satisfy enterprise constraints.

### 14.3 A hybrid approach is often strongest

Use a framework or managed service for generic capabilities, while
owning: - Domain-specific tools. - Identity and authorization. -
Business rules. - Data access. - Approval flows. - Verification. -
Evaluation datasets. - Observability conventions.

Avoid rebuilding commodity infrastructure unless it gives a meaningful
advantage.

### 14.4 Questions before choosing a managed agent platform

1.  Who owns the orchestration loop?
2.  Where does session state live?
3.  Can sessions resume after failures?
4.  Where does code or computer use execute?
5.  Can the runtime connect to private MCP servers?
6.  How are credentials injected and isolated?
7.  Can the application interrupt or steer execution?
8.  How are tool calls and model calls traced?
9.  What are the data retention and residency terms?
10. Can the application export artifacts and audit records?
11. What happens when a provider or tool is unavailable?
12. Can the organization change models without rewriting the workflow?

------------------------------------------------------------------------

## 15. Hands-on learning roadmap

A practical sequence for an engineer building production multi-agent
systems:

### Phase 1 --- Understand the harness

-   Read the primary harness article.
-   Build a minimal model → tool → observation → model loop.
-   Add a strict maximum-step limit.
-   Add typed tool schemas and structured errors.
-   Add a completion verifier.

**Deliverable:** a small agent that reads a workspace, runs a command,
interprets the result, and produces a verified report.

### Phase 2 --- Build a real tool layer with MCP

-   Implement one MCP server.
-   Expose a read-only search tool.
-   Expose a narrowly scoped write tool.
-   Add authentication and authorization.
-   Add input validation, timeouts, and audit logging.
-   Test malicious or malformed tool inputs.

**Deliverable:** a reusable MCP integration that can be connected to
more than one compatible host.

### Phase 3 --- Add state and durable execution

-   Persist task state.
-   Add checkpoints.
-   Support cancellation and resume.
-   Add idempotency for side effects.
-   Add bounded retries and deadlines.

**Deliverable:** a long-running task that survives a worker restart
without duplicating external actions.

### Phase 4 --- Add multi-agent collaboration with A2A

-   Build a coordinator agent.
-   Build one independent specialist agent.
-   Define a task contract and output schema.
-   Add A2A communication.
-   Propagate identity, authorization, and trace context.
-   Verify the specialist's output before using it.

**Deliverable:** two independently deployed agents collaborating through
a documented protocol.

### Phase 5 --- Production hardening

-   Add model routing and fallback.
-   Add policy enforcement and approval queues.
-   Add sandbox isolation.
-   Add OpenTelemetry-compatible traces and metrics.
-   Build an evaluation dataset.
-   Run adversarial and regression tests.
-   Track cost per successful task.

**Deliverable:** a production-ready agent service with measurable
quality, controlled authority, and auditable execution.

### Suggested capstone project

**Enterprise incident investigation multi-agent system**

``` text
Incident event
   |
   v
Coordinator
   |
   +--> Observability agent (MCP: metrics/logs/traces)
   |
   +--> Change-history agent (MCP: deployment records)
   |
   +--> Knowledge agent (MCP: runbooks and documentation)
   |
   +--> Risk reviewer (policy and evidence review)
   |
   v
Evidence synthesizer
   |
   v
Human approval for remediation
   |
   v
Controlled remediation tool
   |
   v
Post-action verification and incident report
```

Design requirements: - All investigation agents are read-only. - Each
finding includes evidence and timestamps. - The coordinator cannot
invent missing evidence. - Remediation is a separate capability
requiring explicit approval. - Every task and subtask shares a
correlation ID. - The system records model, tool, policy, and prompt
versions. - The final report distinguishes verified facts from
hypotheses.

This project demonstrates harness engineering, MCP, A2A, multi-agent
orchestration, security, observability, and evaluation in one realistic
workflow.

------------------------------------------------------------------------

## 16. Glossary

  -----------------------------------------------------------------------
  Term                                Definition
  ----------------------------------- -----------------------------------
  Agent                               A model operating with a harness to
                                      pursue a task

  Agent harness                       Software that manages context,
                                      tools, loops, state, policy,
                                      execution, and verification

  Agentic workflow                    A process in which an AI system
                                      takes multiple steps toward an
                                      outcome

  A2A                                 Agent2Agent Protocol for
                                      interoperable agent communication

  Context engineering                 Selecting and managing information
                                      supplied to a model

  Computer use                        Interacting with a computer
                                      interface through visual or
                                      structured actions

  Foundation model                    General-purpose model trained on
                                      broad data

  Handoff                             Transfer of a task or control from
                                      one agent to another

  MCP                                 Model Context Protocol for
                                      connecting AI applications to tools
                                      and context

  Memory                              Persisted information used across
                                      turns or sessions

  Model gateway                       Layer that routes and governs
                                      model-provider calls

  Orchestration                       Coordination of steps, tools,
                                      agents, and state

  ReAct                               Reasoning-and-acting pattern that
                                      alternates between model decisions
                                      and tool observations

  Runtime                             Environment where agent sessions
                                      and actions execute

  Sandbox                             Isolated environment that limits
                                      execution impact

  Skill                               Reusable instructions or procedures
                                      for a task type

  Tool                                A callable operation exposed to an
                                      agent

  Trace                               Structured record of a task and its
                                      nested operations

  Verification                        Independent check that an expected
                                      result was achieved
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 17. Further reading and references

### Core concept and product taxonomy

1.  Prasenjit Paul --- [What is an AI agent harness? The body around the
    brain](https://paulshan.com/engineering/what-is-an-ai-agent-harness/)
    (September 18, 2026). Primary conceptual source for the
    model/harness/agent distinction and harness anatomy.
2.  Prasenjit Paul --- [ChatGPT, Claude, Gemini, Grok: the map of what
    each AI company
    sells](https://paulshan.com/engineering/ai-product-map/) (October 6,
    2026). Product taxonomy across models, chat apps, coding harnesses,
    always-on agents, and developer platforms.
3.  Google Cloud --- [What is an agent
    harness?](https://cloud.google.com/discover/agent-harness).
    Additional overview of harness responsibilities.

### Agent development platforms

4.  OpenAI --- [Agents
    documentation](https://developers.openai.com/api/docs/guides/agents).
5.  OpenAI --- [Agents API
    overview](https://developers.openai.com/api/docs/guides/agents-api/overview).
6.  OpenAI --- [Building agents learning
    track](https://developers.openai.com/tracks/building-agents).
7.  OpenAI --- [Codex
    documentation](https://developers.openai.com/codex).
8.  Anthropic --- [Claude Code
    documentation](https://docs.anthropic.com/en/docs/claude-code/overview).
9.  Google --- [Agent Development Kit
    documentation](https://google.github.io/adk-docs/).

### Interoperability

10. Model Context Protocol --- [Official
    documentation](https://modelcontextprotocol.io/).
11. Model Context Protocol ---
    [Specification](https://github.com/modelcontextprotocol/modelcontextprotocol).
12. Agent2Agent --- [Official protocol
    documentation](https://a2a-protocol.org/).
13. Agent2Agent --- [Linux Foundation
    project](https://github.com/a2aproject/A2A).

### Open-source agent tools

14. [OpenCode](https://opencode.ai/).
15. [OpenHands](https://www.openhands.dev/).
16. [Aider](https://aider.chat/).
17. [Cline](https://cline.bot/).
18. [LangGraph](https://langchain-ai.github.io/langgraph/).
19. [Ollama](https://ollama.com/).
20. [vLLM](https://docs.vllm.ai/).

------------------------------------------------------------------------

## Final perspective

The AI market is easier to understand when products are classified by
the job they perform:

-   **Models** provide intelligence.
-   **Chat assistants** provide a conversational product.
-   **Coding harnesses** provide repository-level execution.
-   **Always-on agents** provide persistent goal-directed work in an
    environment.
-   **Developer platforms** provide APIs, SDKs, and managed
    infrastructure.
-   **Harness engineering** connects these capabilities into a reliable
    system.

For production engineering, the durable advantage is rarely just
selecting a model. It is building the right context, tools, permissions,
state, execution loop, verification, and observability around it.

**The key question changes from "Which model is smartest?" to "Which
model--harness--environment combination can complete this task safely,
reliably, and measurably?"**
