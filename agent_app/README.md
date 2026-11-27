# Personal agent app: one UI, four agent frameworks

A small but complete app for running a personal assistant. The user picks a framework in the UI, and
the same 200 use cases run on whichever one they chose:

- **LangChain Deep Agents** (`create_deep_agent`)
- **LangGraph** (a hand-built `StateGraph`)
- **Google ADK** (2.x `Agent` + resumable `App`)
- **Claude Agent SDK** (`ClaudeSDKClient` + an in-process MCP tool server)

```
User  ->  UI (one HTML page)  ->  FastAPI  ->  the framework the user prefers
                                     |
                                     +-- SQLite, Postgres or MySQL (one DATABASE_URL)
                                     +-- Redis
```

There's also a live project in the same app: **[real-time order tracking](usecases/order_tracking/README.md)**
at `/orders`. It has three kinds of agent (harness, looping, graph), and each runs on six runtimes: LangChain,
LangGraph, Deep Agents, Google ADK, ADK Workflows and the Claude Agent SDK. A simulated carrier feed streams
through Redis to the browser over Server-Sent Events.

Everything runs offline with no API keys in **scripted** mode. Only the model's decisions are scripted;
the framework, approvals, tools, database and Redis are all real. Switch a user to **live** mode and a real
model makes the decisions instead.

What I checked before shipping:

| Check | Result |
|---|---|
| 200 use cases x 4 frameworks, SQLite + in-process Redis | 800/800 |
| Live order tracking: 3 agent types x 6 runtimes, plus API, SSE and two agents on one stream | 23 tests, also on Postgres and MariaDB |
| Same suite on **Postgres 16** + real Redis 7 | 819 tests passed |
| Same suite on **MariaDB 10.11** (the MySQL driver path) + real Redis | 819 tests passed |
| API flows: approve / edit / reject over HTTP on each framework, guards reading preferences, memory shared across frameworks, background runs, rate limit | passing |
| The UI, clicked through in headless Chrome (pause, edit, resume) | no JS errors |

`docker-compose.yml` passes `docker compose config`, but I couldn't run Docker here. MySQL 8 itself
(rather than MariaDB) wasn't tested either.

## Quick start

```bash
cd agent_app
pip install -r requirements.txt          # Python 3.11+
uvicorn app.api:app --reload             # SQLite file + in-process Redis, no setup
open http://localhost:8000
```

With Postgres and Redis:

```bash
docker compose up --build                # app + postgres + redis
docker compose --profile mysql up        # adds MySQL; switch DATABASE_URL in the compose file
```

Without the UI:

```bash
python usecases/048_move_money_to_savings/usecase.py --all       # one use case on all four frameworks
python usecases/048_move_money_to_savings/usecase.py --manual    # you answer the approval in the terminal
python scripts/run_all.py                                        # all 800 runs, summary table
python -m pytest -q                                              # 842 tests
```

## Architecture

```mermaid
flowchart LR
    UI["UI<br/>ui/index.html"] -->|REST| API["FastAPI<br/>app/api.py"]
    API --> SVC["Run service<br/>app/service.py"]
    SVC -->|"user's framework preference"| REG{"Runtime registry"}
    REG --> DA["Deep Agents<br/>interrupt_on"]
    REG --> LG["LangGraph<br/>interrupt in a gate node"]
    REG --> ADK["Google ADK<br/>tool confirmation"]
    REG --> CL["Claude Agent SDK<br/>can_use_tool"]
    DA --> TL["Shared tool layer<br/>app/tools.py"]
    LG --> TL
    ADK --> TL
    CL --> TL
    TL -->|"guards read preferences"| P[("preferences")]
    TL -->|"read-tool cache"| R[("Redis")]
    TL -->|"tool calls, memory"| DB[("SQLite / Postgres / MySQL")]
    SVC -->|"runs, events"| DB
    API -->|"rate limit, locks, pref cache"| R
    CL -->|"approval hand-off"| R
```

The idea is a small, strict contract. A **use case** (`app/spec.py`) is plain data: tools, steps,
approvals, guards, preference defaults and checks. It knows nothing about frameworks. Each **runtime**
(`app/runtimes/*.py`) turns that data into its framework's own objects. It implements just two methods:
`start(ctx)` and `resume(ctx, decisions)`. Both return either "done, here's the answer" or "paused,
these actions need a decision".

All tool calls from all four frameworks go through one **tool layer** (`app/tools.py`). That's why
behaviour matches across frameworks. The tool layer:

- checks guards first, passing in the user's preferences;
- serves read-only tools from the Redis cache;
- records every call in the database (`ok`, `cached`, `blocked` or `rejected`);
- implements `remember` / `recall` against the `memories` table, so memory written under ADK can be read
  under Claude.

## A run, start to finish

```mermaid
sequenceDiagram
    participant U as UI
    participant A as FastAPI
    participant S as Run service
    participant F as Framework runtime
    participant T as Tool layer
    participant D as Database
    U->>A: POST /api/runs {usecase_id: 48}
    A->>S: create_run (framework from preferences)
    S->>D: insert run
    S->>F: start(ctx)
    F->>T: checking_balance()
    T->>D: record tool call
    F-->>S: paused: transfer(amount=500)
    S->>D: status = awaiting_approval, pending = [...]
    S-->>U: run with pending action
    U->>A: POST /api/runs/{id}/decisions [edit amount=250]
    A->>S: decide (Redis lock on the run)
    S->>F: resume(ctx, decisions)
    F->>T: transfer(amount=250)
    T->>D: record tool call
    F-->>S: done, final answer
    S->>D: status = done, checks
    S-->>U: final answer + tool calls
```

## How each framework pauses for a person

Every runtime uses its framework's own human-in-the-loop mechanism. None is a homemade imitation.

| Framework | How it pauses | How it resumes | Edit / reject |
|---|---|---|---|
| Deep Agents | `interrupt_on={tool: {...}}` + checkpointer; the result has `__interrupt__` with `action_requests` | `Command(resume={"decisions": [...]})` | `{"type": "edit", "edited_action": {...}}`, `{"type": "reject", "message": ...}` |
| LangGraph | A `gate` node between `agent` and `tools` calls `interrupt()` once per turn for all gated calls. It has no side effects, so re-running it on resume is safe | `Command(resume={"decisions": [...]})` | The gate rewrites the AI message (same id) with the approved or edited calls and adds a `ToolMessage` for each rejection |
| Google ADK | A `BaseTool` calls `tool_context.request_confirmation()`; the app has `ResumabilityConfig(is_resumable=True)`, so the invocation stops | A `FunctionResponse` named `adk_request_confirmation` with `{"confirmed": ...}`, sent with the same `invocation_id` | Edits go in the confirmation `payload`; `confirmed: false` rejects |
| Claude Agent SDK | The SDK awaits the `can_use_tool` callback. The callback reports "paused" and then waits for a decision on a Redis list | `cache.push_decisions()` from the API request | `PermissionResultAllow(updated_input=...)`, `PermissionResultDeny(message=...)` |

Parallel calls work everywhere. Use case #23 asks to unsubscribe from three senders in one turn, and the
test approves two and rejects one on each framework.

### How the Claude Agent SDK runs offline

The SDK normally talks to the `claude` CLI over a JSON stream. `ScriptedCLI` in `app/runtimes/claude_rt.py`
is a `Transport` that plays the CLI's side of that protocol: it emits the assistant messages, asks
`can_use_tool` through a control request, and does the MCP `initialize` handshake. It then calls the
tools on the app's in-process MCP server with `tools/call`. The SDK client, the permission callback and
the MCP server are all the real ones. In live mode the transport is the bundled CLI, and Claude makes
the decisions.

## Preferences decide what runs

Each user has preferences in the database. They're cached in Redis and edited in the UI:

| Preference | What it does |
|---|---|
| `framework` | `deepagents`, `langgraph`, `adk` or `claude`. Every run uses it unless the request names one |
| `mode` | `scripted` (no keys) or `live` |
| `lc_model`, `adk_model`, `claude_model` | Per-user model choice in live mode |
| `home_city`, `diet`, `partner`, `kid`, `dog`, `seat_preference`, ... | Filled into use cases through `{placeholders}`. Set `home_city` to Denver and the morning brief fetches Denver weather |
| `max_purchase_without_review`, `monthly_grocery_budget` | Read by guards. Raise the limit and use case #56 buys the laptop; leave it at $200 and it's blocked |

The order is: built-in defaults (`config.DEFAULT_PROFILE`), then what a use case needs, then the user's
saved preferences, which win.

## Database

```mermaid
erDiagram
    users ||--o{ preferences : has
    users ||--o{ runs : starts
    users ||--o{ memories : keeps
    runs ||--o{ tool_calls : records
    runs ||--o{ events : logs
    runs {
        string id
        string framework
        string mode
        string status
        json pending
        json checks
    }
    tool_calls {
        string tool
        json args
        json result
        string effect
        string status
    }
    memories {
        string key
        text value
    }
```

One SQLAlchemy model set; the URL picks the engine:

```bash
DATABASE_URL=sqlite:///./agent_app.db
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/agent_app
DATABASE_URL=mysql+pymysql://app:app@localhost:3306/agent_app
```

Tables are created on startup. For a real deployment, add Alembic migrations.

## Redis

| Key | Used for |
|---|---|
| `cache:tool:{tool}:{hash}` | Results of read-only tools, with a TTL (`TOOL_CACHE_TTL`). These show as `cached` in the tool-call list |
| `prefs:{user}` | Preference cache, dropped when preferences change |
| `ratelimit:{user}:{minute}` | Runs per user per minute; the API returns 429 past `RATE_LIMIT_PER_MIN` |
| `lock:run:{id}` | One decision at a time per run (two clicks don't resume twice) |
| `decisions:{run id}` | How a decision reaches a Claude run waiting inside `can_use_tool` |

If `REDIS_URL` is empty, the app uses `fakeredis` in the same process, so a laptop needs nothing extra.

## API

| Method | Path | |
|---|---|---|
| GET | `/api/health` | Database engine, Redis kind, which frameworks are installed |
| GET | `/api/frameworks` | The four frameworks and whether each is installed |
| GET | `/api/usecases?area=&q=` | The catalogue |
| GET | `/api/usecases/{id}?user_id=` | One use case, with steps filled in from that user's preferences |
| GET / PUT | `/api/users/{id}/preferences` | Read or merge preferences |
| GET | `/api/users/{id}/memories` | Long-term memory |
| GET | `/api/users/{id}/runs` | Recent runs |
| POST | `/api/runs?wait=true` | Start a run. `{"usecase_id", "framework"?, "mode"?, "auto_approve"?, "message"?}`. With `wait=false` it returns the id at once and you poll |
| GET | `/api/runs/{id}` | Status, pending actions, tool calls, events, checks |
| POST | `/api/runs/{id}/decisions` | `{"decisions": [{"type": "approve"}, {"type": "edit", "args": {...}}, {"type": "reject", "message": "..."}]}`, one per pending action |

Interactive docs are at `/docs`.

## The 200 use cases

They cover one person, Sam, across ten areas of life, 20 each:

1. mornings
2. email and calendar
3. money
4. errands
5. travel
6. home and family
7. fitness and food
8. work
9. learning
10. digital life

See [usecases/README.md](usecases/README.md). Each folder has `usecase.py` and a README with its flow,
tools, approvals, guards and the preferences it uses.

The features they use:

- approvals: 75
- parallel calls: 73
- memory: 58
- preference placeholders: 48
- guards: 17

Adding one is a new folder:

```python
# usecases/201_water_the_plants/usecase.py
USECASE = UseCase(
    id=201, area="home", title="Water the plants",
    ask="Water the balcony plants if it isn't going to rain.",
    why="Checks the forecast before turning on the drip system.",
    tools=[T("get_weather", "Weather for a city.", {"city": str}, {"rain_next_12h": False}),
           T("start_drip", "Run the drip system.", {"minutes": int}, "running", "write")],
    steps=[call("get_weather", city="{home_city}"), call("start_drip", minutes=10), answer("No rain coming, so the plants got 10 minutes.")],
    approvals={"start_drip": "approve"},
)
```

Then run `python scripts/gen_readmes.py` and it shows up in the UI.

## Scripted and live

In **scripted** mode each framework gets a stand-in model that replays the use case's `steps`:

- LangChain's `GenericFakeChatModel` for Deep Agents and LangGraph;
- a `BaseLlm` subclass for ADK;
- the `ScriptedCLI` transport for Claude.

That's what makes 800 runs take about 30 seconds and lets the tests assert exact outcomes.

In **live** mode the steps are ignored and a real model decides:

| Framework | Model setting | Key |
|---|---|---|
| Deep Agents / LangGraph | `LC_MODEL` (for example `anthropic:claude-sonnet-5-5`, needs `langchain-anthropic`) | the provider's key |
| ADK | `ADK_MODEL`. A Gemini name uses `GOOGLE_API_KEY`; `provider/model` goes through LiteLLM | `GOOGLE_API_KEY` or the provider's key |
| Claude Agent SDK | `CLAUDE_MODEL` | `ANTHROPIC_API_KEY` |

Tools still return the canned data until you replace them. Approvals and guards behave exactly the same.

## Going to production

What's here is honest about what it is: one process, built to show the moving parts clearly. To run it
for real:

1. **Persist paused runs.** Paused agents live in memory in the worker that started them. Swap in:
   - LangGraph's `PostgresSaver` (in `deepagents_rt.py` / `langgraph_rt.py`);
   - ADK's `DatabaseSessionService(db_url=...)` (in `adk_rt.py`).
   
   A paused run then survives a restart and can resume on any worker. The Claude runtime already hands
   decisions over through Redis; what's left is routing the resume to the worker that holds the session,
   or using the SDK's session resume.
2. **Run more than one worker** only after step 1. Until then use `--workers 1`, which is what the
   Dockerfile does.
3. **Replace the canned tools.** Swap `T(..., returns=...)` for real calls: your APIs, a CLI, or MCP
   servers (`langchain-mcp-adapters` for LangChain, `McpToolset` for ADK, `mcp_servers=` for Claude).
4. **Add auth.** `user_id` is currently whatever the client sends. Put the API behind your identity
   provider and take the user from the token.
5. **Keep guards in code.** They live in the tool layer, so a confused model can't talk its way past a
   spending limit.
6. **Add tracing.** LangSmith for the LangChain side; OpenTelemetry works across all four.
7. **Use migrations** (Alembic) instead of `create_all`.

## Layout

```
agent_app/
  app/
    api.py              FastAPI routes + serves the UI
    service.py          start / pause / decide / checks, persistence
    spec.py             the framework-neutral use-case format
    tools.py            shared tool layer: guards, Redis cache, DB recording, memory
    db.py               SQLAlchemy models (SQLite / Postgres / MySQL)
    cache.py            Redis helpers (real or fakeredis)
    config.py           settings from env
    cli.py              run one use case from the terminal
    usecases.py         loads usecases/NNN_*/usecase.py
    runtimes/
      deepagents_rt.py  langgraph_rt.py  adk_rt.py  claude_rt.py  lc_common.py  base.py
  ui/index.html         the whole UI, no build step
  usecases/             200 folders, one per use case, + README.md catalogue
    order_tracking/     live project: 3 agent types x 6 runtimes, SSE, Redis streams (own README)
  scripts/              run_all.py, gen_readmes.py
  tests/                test_usecases.py (800 runs), test_api.py
  Dockerfile  docker-compose.yml  requirements.txt  .env.example  Makefile
```
