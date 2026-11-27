"""Writes services/*/README.md. Kept as a script so the docs stay in one place and easy to edit.

    python docs/gen_service_readmes.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "services"

S = {}

S["s01_grok_bot"] = dict(
    title="01 - Grok Bot (SpaceXAI / xAI, on Cursor infrastructure)",
    file="grok_bot.py",
    what="""Persistent, named Bots (a name, a job title, a description) that work on a persistent cloud computer with a browser, filesystem and terminal. Bots share that computer but keep their own memory, learn a routine when you walk them through a task once, run Routines on a schedule, coordinate with each other, and ask before sensitive steps. They reach apps through connectors, plugins and MCP, and through computer use when no connector exists. Early beta opened on Aug 11 2026, for macOS, Windows, Linux and iOS.""",
    api="""**No public Grok Bot API** (no list/create bot, send message, read reply). Two official programmable surfaces exist: the **xAI API** via `xai-sdk` (server-side tools `web_search`, `x_search`, `code_execution` plus your own client-side tools), and the **Cursor Python SDK** cloud agents, the runtime family Grok Bot lives on.""",
    diagram="""flowchart TB
    subgraph Account
      C[(Shared cloud computer<br/>files, browser, terminal)]
      F[Finn - Finance Ops<br/>own memory]
      R[Ria - Research<br/>own memory]
      T[[Team thread]]
      RT[Routine 07:30]
    end
    RT --> F
    F <--> T <--> R
    F --> C
    R --> C
    F -. approval .-> U((You))""",
    mapping=[("Shared computer", "`GrokBotAccount.computer` (one `SandboxComputer`)"),
             ("Per-Bot memory", "`Memory(spec.name, ...)` per Bot"),
             ("Teach once", "`GrokBotAccount.teach()` writes `skills/<name>/SKILL.md`"),
             ("Routines", "`Scheduler` + `Routine(at='07:30')`"),
             ("Bot-to-Bot", "`ask_bot` tool + `thread`"),
             ("Approvals", "`ApprovalGate(RISK_BASED)`; the scripted you refuses `pay`"),
             ("Live Bot", "`LiveGrokBot`: xai-sdk chat, server + client tools, `~/.grokbots/<name>.json`")],
    live="pip install xai-sdk   # optional: cursor-sdk\nexport XAI_API_KEY=...  # optional: CURSOR_API_KEY=crsr_...\npython -m services.s01_grok_bot.grok_bot --live",
    notes=["Server-side tool calls run on xAI's servers; only `client_side_tool` calls come back to your loop. Check with `get_tool_call_type`.",
           "xAI says separate Bots are not separate security boundaries. The mock mirrors that: one computer, one skills folder.",
           "The model name defaults to `grok-4.7`; set `XAI_MODEL` to whatever your account has."])

S["s02_openai_dots"] = dict(
    title="02 - dots (OpenAI)", file="dots.py",
    what="""Always-on personal agents in ChatGPT, launched at DevDay on Sep 29 2026 for Pro and Business Premium. You start with a primary dot, name it, and connect calendar, email, your computer and other tools. It works in the background without prompting, and you can message it from ChatGPT, Codex, Slack and Teams. Specialist dots with their own identities and teams of dots are planned.""",
    api="""No public dots API. The live mode is a build-alike on the **OpenAI Agents SDK** (`openai-agents`).""",
    diagram="""flowchart LR
    BG[Background pass<br/>read-only tools] -->|finding| U((You in Slack))
    U -->|"yes, do it"| FG[Foreground run<br/>all tools]
    FG -->|send?| U
    FG --> Apps[(Mail, Calendar, Stripe)]
    BG --> Apps""",
    mapping=[("Read-only background research", "`ApprovalMode.DENY_ALL` and `ToolRegistry.subset(Risk.READ)`; `send_email` isn't even offered"),
             ("Prepare then act after approval", "`ApprovalMode.RISK_BASED`"),
             ("Primary dot with memory", "`Memory('Pip')` shared by both runs"),
             ("Live", "two `agents.Agent`s: a read-only background agent and an approval-gated foreground agent")],
    live="pip install openai-agents\nexport OPENAI_API_KEY=...\npython -m services.s02_openai_dots.dots --live",
    notes=["OpenAI says dots' unprompted background research uses read-only tools, so it can't send messages, change apps or drive a browser. Copy that rule.",
           "The mock's proactive pass finds a real mismatch in the seed data: PyConf confirmed Wednesday Dec 9, the calendar says Tuesday."])

S["s03_claude_duet"] = dict(
    title="03 - Claude Duet (Anthropic)", file="claude_duet.py",
    what="""A research preview (Oct 21 2026, US Pro and Max, waitlist) of Claude as a proactive agent you message like a person. It sends a short morning brief across connected apps, checks connected accounts every few hours instead of continuously, uses the same memories, skills and connectors as regular Claude, keeps working on a cloud computer after the app closes, and has Stripe (unpaid invoices, drafted reminders) and Link / Shop Pay (purchases with approval) integrations. Runs on Claude Opus 5.5.""",
    api="""No public Duet API. The live mode rebuilds the pattern with the **Claude Agent SDK**: in-process MCP tools, a `can_use_tool` permission callback, a multi-turn `ClaudeSDKClient`.""",
    diagram="""sequenceDiagram
    participant S as Scheduler
    participant D as Duet
    participant A as Apps
    participant U as You
    loop every 3h
      S->>D: check
      D->>A: read-only checks
    end
    S->>D: 07:00 brief
    D->>U: "Needs you today: ..."
    U->>D: send
    D->>U: approve send_email?
    U-->>D: yes
    D->>A: send""",
    mapping=[("Every few hours", "`Routine('check-connected-apps', every_minutes=180)`"),
             ("Morning brief", "`Routine('morning-brief', at='07:00')`"),
             ("Needs your attention", "the `attention` list built by the checks"),
             ("Act with approval", "`ApprovalMode.RISK_BASED`; live: `can_use_tool` returns `PermissionResultDeny`")],
    live="pip install claude-agent-sdk\nexport ANTHROPIC_API_KEY=...\npython -m services.s03_claude_duet.claude_duet --live",
    notes=["Anthropic says the background work counts against the same usage limits as chat. Cheap read-only checks plus one brief is the economical shape.",
           "In the SDK, MCP tool names look like `mcp__<server>__<tool>`; match on that in `can_use_tool` and `allowed_tools`."])

S["s04_gemini_task"] = dict(
    title="04 - Gemini Task (Google, formerly Gemini Spark)", file="gemini_task.py",
    what="""Google's personal agent, launched as Gemini Spark in May 2026 and renamed Task in the autumn (now a Chat | Task toggle, with a Scheduled page). Three primitives: **Tasks**, **Schedules** ("Every Monday at 9:00 AM..."), **Skills** ("turn my last 50 emails into a style guide called ghostwriter"). It connects to Gmail, Calendar, Docs, Sheets, Slides, Keep and Tasks, browses with Chrome auto browse or a remote browser, asks before browsing, and stops for you to take over at sign-in pages or when sensitive info is needed.""",
    api="""No public Task API. The Google-native way to build the same thing is **ADK** + Gemini; ADK's `before_tool_callback` is the approval hook.""",
    diagram="""flowchart LR
    SK[(Skill: ghostwriter)] --> T[Task run]
    T -->|draft| G[Gmail]
    T -->|open portal| B[Remote browser]
    B -->|SIGN_IN_REQUIRED| U((You take over))
    U --> T
    SC[Schedule Mon 09:00] --> R[Inbox recap]""",
    mapping=[("Skills", "`SkillStore` with `ghostwriter`, injected into the system prompt"),
             ("Take-over at sign-in", "`SandboxComputer.open()` returns `SIGN_IN_REQUIRED`; `take_over` tool pauses for you"),
             ("Schedules", "`Routine('monday-recap', at='09:00')`"),
             ("Confirm major actions", "live: ADK `before_tool_callback` returning a dict skips the real tool")],
    live="pip install google-adk\nexport GOOGLE_API_KEY=...\npython -m services.s04_gemini_task.gemini_task --live",
    notes=["Google's help page tells users not to type sign-in or payment details into the task thread; take over the browser instead. The `take_over` tool encodes that."])

S["s05_meta_muse"] = dict(
    title="05 - Muse (Meta)", file="muse.py",
    what="""Meta's personal agent (Sep 8 2026), powered by Muse Spark. Each person's Muse runs on **Muse Secure VM**, a dedicated VM holding the agent and that person's data and credentials. A separate **Sentinel** agent runs on the same machine, kept apart from Muse at the system level: nothing Muse does reaches the internet unless Sentinel approves it, and Sentinel asks the person when needed. Purchases go through Link by Stripe. Available as an app, at muse.ai and in WhatsApp; free tier plus $20 and $100 plans.""",
    api="""No public API. Mock = the architecture. Live = the same worker + Sentinel design on any OpenAI-compatible model.""",
    diagram="""flowchart LR
    subgraph VM[Muse Secure VM]
      M[Muse worker] --> S{Sentinel}
    end
    S -->|allowed| NET((Internet))
    S -.->|ask| U((You))
    S -->|blocked| X[x]""",
    mapping=[("Secure VM", "`MuseSecureVM` builds the agent *and* its Sentinel; the agent can't configure its own checker"),
             ("Sentinel", "`Sentinel(allowed_domains, allowed_channels, blocked_terms, human)`"),
             ("Worker doesn't gate", "`ApprovalGate(ApprovalMode.AUTO)` on purpose; control is at egress"),
             ("Link checkout caps", "`Budget(limit=100)`")],
    live="export PA_BASE_URL=... PA_API_KEY=... PA_MODEL=...\npython -m services.s05_meta_muse.muse --live",
    notes=["The injected page in the mock tries to email a card number to a look-alike domain. The Sentinel never reads the page; it only sees the outgoing action, which is why the trick doesn't work on it."])

S["s06_copilot_cowork"] = dict(
    title="06 - Microsoft 365 Copilot Cowork", file="copilot_cowork.py",
    what="""Cowork carries out tasks across Microsoft 365: sends email, schedules meetings, creates documents, posts in Teams, manages your calendar. It grounds on your work context, plans, then executes, and **you approve each action before it happens**. Skills load during a session (shown in a side panel); plugins from the Microsoft 365 App Store add skills and connectors (Accounting, Finance, Capital Markets). Generally available since Jun 16 2026, usage-based billing, and at GA it ran on Anthropic models.""",
    api="""No public "run a Cowork task" API; extension is through plugins, Copilot Studio and Agent 365. Live = the same approve-every-action loop on any OpenAI-compatible endpoint, including Azure OpenAI.""",
    diagram="""flowchart LR
    P[Plugin: Accounting] --> SK[(skills)]
    G[Goal] --> PL[Plan shown]
    PL --> A1[step] -->|approve?| U((You))
    U --> A2[step] -->|approve?| U""",
    mapping=[("Approve every action", "`ApprovalMode.EVERY`"),
             ("Plan first", "`show_plan` tool as the first step"),
             ("Plugins add skills", "`ACCOUNTING_PLUGIN` -> `SkillStore`")],
    live="export PA_BASE_URL=https://<your-azure-openai>/openai/v1 PA_API_KEY=... PA_MODEL=<deployment>\npython -m services.s06_copilot_cowork.copilot_cowork --live",
    notes=["Approving everything is safe and slow. The mock counts 6 prompts for one morning routine; that's the trade-off Microsoft chose for enterprise."])

S["s07_manus_cue"] = dict(
    title="07 - Cue (Manus)", file="cue.py",
    what="""Launched with Manus 2.0 on Sep 28 2026. Each Cue agent has its **own email address, phone number, wallet and computer**. It can take forwarded calls and summarize them, send and receive mail from its own address, pay within limits you set, and keep working after you log off. Several agents can join one group chat and hand work to each other while you steer.""",
    api="""No separate public Cue API was documented at launch; live mode sends the work to the **Manus v2 API** (`s11`) with identity rules in the task.""",
    diagram="""flowchart LR
    subgraph Cole[Agent Cole]
      E1["cole@agents.cue.im"]
      P1["+1 phone"]
      W1["wallet $0"]
    end
    subgraph Ezra[Agent Ezra]
      E2["ezra@agents.cue.im"]
      W2["wallet $50"]
    end
    Cole --> GC[[Group chat]]
    Ezra --> GC
    U((You)) --> GC""",
    mapping=[("Per-agent identity", "`Identity(email, phone, wallet, computer)`"),
             ("Own address", "`send_as_agent` sends from the agent's email, never yours"),
             ("Calls", "`take_call` writes a summary"),
             ("Wallet", "`Budget` per agent; Ezra's $40 upgrade is refused with $26 left"),
             ("Group chat", "`group_chat` tool")],
    live="export MANUS_API_KEY=...\npython -m services.s07_manus_cue.cue --live",
    notes=["Identity separation is a blast-radius control: the test asserts the user's own outbox stays empty."])

S["s08_openclaw"] = dict(
    title="08 - OpenClaw (open source)", file="openclaw.py",
    what="""A personal AI assistant you run on your own devices (MIT licensed, formerly Clawdbot, then Moltbot). It answers on the channels you already use (WhatsApp, Telegram, Slack, Discord, Signal, iMessage, Teams, Matrix, WebChat...), routes channels and peers to isolated agents with their own workspaces and sessions, runs heartbeats and cron, installs skills from ClawHub, and works with Claude, GPT and other models. Main-session tools run on the host with full access, so run it somewhere you're comfortable with that.""",
    api="""The Gateway can serve OpenAI-compatible endpoints, including an OpenResponses `POST /v1/responses` (disabled by default, full operator access once authenticated). Select an agent with `model="openclaw:<agentId>"`; pass `user` for a stable session.""",
    diagram="""flowchart LR
    WA[WhatsApp] --> GW{Gateway}
    SL[Slack] --> GW
    TG[Telegram stranger] -.->|dropped| GW
    GW -->|main| A1[Agent main]
    GW -->|work| A2[Agent work]
    HB[heartbeat] --> A1
    CH[(ClawHub skills)] --> A1""",
    mapping=[("Gateway", "`Gateway` class: `routes`, `owner_ids`, `dm_policy`, `sessions`"),
             ("Isolated agents", "two `AutonomousAgent`s with separate memory"),
             ("DM allowlist", "`inbound()` drops unknown peers unless `dm_policy='open'`"),
             ("Heartbeats", "`Routine('heartbeat', every_minutes=60)`"),
             ("ClawHub", "`SkillStore` with `invoice-chaser`")],
    live="# in OpenClaw config: gateway.http.endpoints.responses.enabled = true\nexport OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789 OPENCLAW_GATEWAY_TOKEN=...\npython -m services.s08_openclaw.openclaw --live",
    notes=["Use the port your gateway prints; 18789 is just the example default here.",
           "Anyone with the gateway token is an operator. Don't expose the endpoint publicly."])

S["s09_instinct"] = dict(
    title="09 - Instinct (Spear Street Technology)", file="instinct.py",
    what="""An invite-only personal agent you **text or call**: no new interface. It connects to mail, messaging, calendar and devices, is trained to use a phone and a computer like a person, and runs on a persistent cloud computer with cached credentials on the company's servers. Not self-hostable; no published pricing; privacy is the main criticism.""",
    api="""No public API. Mock = an SMS thread in front of the agent loop with approvals inside the thread. Live = the same with a real model; point `on_sms` at a Twilio-style webhook to make it real.""",
    diagram="""sequenceDiagram
    participant U as You (SMS)
    participant W as Webhook
    participant A as Agent
    U->>W: "morning ops pls"
    W->>A: run(goal)
    A->>U: OK to send email -> ap@northwind.com? YES/NO
    U-->>A: YES
    A->>U: OK to send email -> maria@...?
    U-->>A: NO
    A->>U: summary""",
    mapping=[("Text interface", "`SmsThread`"),
             ("In-thread approval", "`ask_by_text` as the gate's `human`"),
             ("Webhook", "`InstinctLike.on_sms(body)`")],
    live="export PA_BASE_URL=... PA_API_KEY=... PA_MODEL=...\npython -m services.s09_instinct.instinct --live",
    notes=["If you build this for real, put a timeout on approvals and treat silence as NO."])

S["s10_perplexity_personal_computer"] = dict(
    title="10 - Perplexity Personal Computer", file="personal_computer.py",
    what="""A local agent harness (Mac in April 2026, Windows in July) that orchestrates sub-agents across your local files, native apps and the web, connected to Perplexity's servers and many frontier models. Recommended on an always-on Mac mini. The safety pitch: explicit approval for sensitive actions, a complete audit log, files in a secure sandbox, actions that are auditable and reversible. Perplexity opened four of the APIs behind it: Search, Agent, Embeddings, Sandbox.""",
    api="""The **Agent API** (`POST /v1/agent`, also `/v1/responses` for OpenAI SDK compatibility) via `pip install perplexityai`, with presets such as `pro-search`.""",
    diagram="""flowchart LR
    G[Goal] --> A[Agent]
    A --> FS[(Local sandbox files)]
    A --> SH[Allowlisted shell]
    FS --> AU[(Audit log)]
    SH --> AU
    U((You)) -->|undo| AU""",
    mapping=[("Sandbox files", "`SandboxComputer.files`"),
             ("Audit log", "`SandboxComputer.audit_report()`"),
             ("Reversible", "every write stores an undo closure; `undo_last()`"),
             ("Shell guard", "`rm` isn't on the allowlist, so it's logged as `shell_denied`"),
             ("Live research", "`Perplexity().responses.create(preset='pro-search', input=...)` then `resp.output_text`")],
    live="pip install perplexityai\nexport PERPLEXITY_API_KEY=...\npython -m services.s10_perplexity_personal_computer.personal_computer --live",
    notes=["Reversibility is a property of each tool, not of the agent. Design write tools so they can record how to undo themselves."])

S["s11_manus"] = dict(
    title="11 - Manus (autonomous task execution)", file="manus.py",
    what="""A general agent platform: hand it a task, it plans and works on its own cloud computer (browser, code, files) and returns results and attachments. Manus 2.0 (Sep 28 2026) added Cascade, Studio, Automations and the Cue app.""",
    api="""REST **v2**: `POST /v2/task.create`, `GET /v2/task.detail`, `GET /v2/task.listMessages`, `POST /v2/task.sendMessage`. Header `x-manus-api-key` (or OAuth for Open Apps). Responses are wrapped as `{"ok": true, "request_id": ...}`. Files are deleted 48 hours after upload. Webhooks for production. There's also an OpenAI-compatible Responses surface.""",
    diagram="""sequenceDiagram
    participant C as Your code
    participant M as Manus
    C->>M: task.create {message}
    M-->>C: task_id, task_url
    loop until terminal
      C->>M: task.detail
      M-->>C: running...
    end
    M-->>C: completed + attachments""",
    mapping=[("Client", "`ManusClient` (create, detail, messages, send, wait)"),
             ("Envelope errors", "`_check()` raises on `ok: false` with the `request_id`"),
             ("Mock server", "`FakeManus` with the same lifecycle")],
    live="pip install requests\nexport MANUS_API_KEY=...\npython -m services.s11_manus.manus --live",
    notes=["Status names and the exact detail envelope are read defensively (`status_of`). Check the current reference if polling never ends."])

S["s12_hermes_agent"] = dict(
    title="12 - Hermes Agent (Nous Research)", file="hermes.py",
    what="""An open-source (MIT) self-improving agent launched Feb 26 2026: terminal-native, persistent memory in `~/.hermes`, a messaging gateway, built-in cron that delivers to any platform, subagents, and a **closed learning loop** that creates and refines skills from experience. Skills use the portable SKILL.md format and can come from community hubs with quarantine and audit. Works with Nous Portal, OpenRouter, OpenAI or any endpoint.""",
    api="""It's a harness you install (`curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`). I didn't find a documented programmatic API, so live mode reproduces the learning loop on pa_core with a real model.""",
    diagram="""flowchart LR
    R1[Run 1<br/>explore] --> D[Distil SKILL.md]
    D --> S[(skills/)]
    S --> R2[Run 2<br/>skill in context]
    R2 --> D""",
    mapping=[("Learning loop", "`AutonomousAgent(learn_skills=True)` writes a skill in `_reflect()`"),
             ("Skill reuse", "`SkillStore.match(goal)` injects it into the next system prompt"),
             ("Memory on disk", "`Memory('hermes', home)` JSON")],
    live="export PA_BASE_URL=https://openrouter.ai/api/v1 PA_API_KEY=... PA_MODEL=...\npython -m services.s12_hermes_agent.hermes --live",
    notes=["Auto-written skills are code you didn't review. Hermes quarantines hub skills for that reason; review self-written ones before trusting them with external actions."])

S["s13_genspark"] = dict(
    title="13 - Genspark (AI workspace and agents)", file="genspark.py",
    what="""An AI workspace that pivoted from search to no-code personal agents: AI Slides, Sheets, Docs, "Call For Me" phone calls, an AI browser, Genspark Claw, and a mixture-of-agents engine that cross-checks several frontier models.""",
    api="""A hosted **remote MCP server** at `/api/mcp` on Genspark's host, over streamable HTTP, behind OAuth 2.1 (authorization code + PKCE, refresh tokens, dynamic client registration). No widely documented REST API beyond that.""",
    diagram="""flowchart LR
    A[Your agent] -->|MCP client| S[Genspark MCP server]
    S --> T1[deep_research]
    S --> T2[create_slides]
    S --> T3[call_for_me]""",
    mapping=[("MCP server", "`FakeMCPServer` (list_tools / call_tool)"),
             ("Adapter", "`mcp_tools_as_local()` turns remote tools into `Tool`s with risk levels"),
             ("Live client", "`mcp` SDK `ClientSession` over streamable HTTP with a bearer token; works with mcp 1.x and 2.x")],
    live="pip install mcp httpx\nexport GENSPARK_MCP_URL=... GENSPARK_MCP_TOKEN=...  # token from Genspark's OAuth flow\npython -m services.s13_genspark.genspark --live",
    notes=["The adapter is the reusable part: any MCP server becomes agent tools the same way. Assign risk levels yourself; MCP annotations are hints, not guarantees."])

S["s14_perplexity_comet"] = dict(
    title="14 - Perplexity Comet (AI browser)", file="comet.py",
    what="""A Chromium browser with an agent built in. It reads the page you're on and can click, type and navigate with your signed-in sessions. That's the power and the risk: every page is untrusted input, and indirect prompt injection is the main attack on browser agents.""",
    api="""No public automation API. Live mode shows the open equivalent: Playwright reads the page, the agent decides, read-only by default.""",
    diagram="""flowchart LR
    P[Page text] -->|wrapped as untrusted| A[Agent]
    A -->|navigate| AL{Task allowlist}
    AL -->|ok| B[Browser]
    AL -->|blocked| X[x]
    A -->|submit form| U((approve?))""",
    mapping=[("Untrusted content", "`<untrusted_page>` wrapping + injection heuristics"),
             ("Allowlist per task", "`CometLikeBrowser(allowed_hosts)`"),
             ("Confirm submits", "`submit_form` is `Risk.EXTERNAL`")],
    live="pip install playwright openai && playwright install chromium\nexport PA_BASE_URL=... PA_API_KEY=... PA_MODEL=...\npython -m services.s14_perplexity_comet.comet --live",
    notes=["The injection check is a heuristic for logging. The allowlist is what actually stops the exfiltration."])

S["s15_cursor"] = dict(
    title="15 - Cursor (coding agent, local and cloud)", file="cursor_agent.py",
    what="""Cursor's agent runs locally against your working tree or in an isolated Cursor-hosted VM with your repo cloned in. The Python SDK hides the difference. The same cloud infrastructure hosts Grok Bot, and Cursor's Agent SDK (`@grok/agent-sdk`) deploys agents-as-code.""",
    api="""`pip install cursor-sdk`: `Agent.create(local=LocalAgentOptions(cwd=...))` or `Agent.create(cloud=CloudAgentOptions(repos=[CloudRepository(url, starting_ref)]))`, then `agent.send(prompt).wait().result`. REST: Cloud Agents API `POST /v1/agents` (public beta).""",
    diagram="""flowchart LR
    C[Your code] --> SDK[cursor-sdk]
    SDK -->|local| WT[Working tree]
    SDK -->|cloud| VM[Cursor VM<br/>repo cloned]
    VM --> PR[Pull request]""",
    mapping=[("Run lifecycle", "`FakeCloudRun.wait()`"),
             ("Live", "local runtime by default; cloud if `CURSOR_REPO_URL` is set")],
    live="pip install cursor-sdk\nexport CURSOR_API_KEY=crsr_...  # optional CURSOR_REPO_URL\npython -m services.s15_cursor.cursor_agent --live",
    notes=["The Cloud Agents API runs agent workflows; it isn't a chat-completions endpoint."])

S["s16_devin"] = dict(
    title="16 - Devin (Cognition)", file="devin.py",
    what="""An autonomous software engineer. A session is a cloud machine with a shell, editor and browser that works a prompt until it's done, asking in the session thread when it's blocked.""",
    api="""REST **v3** with service users and RBAC (keys start with `cog_`): `POST /v3/organizations/{org_id}/sessions`, `GET .../sessions/{devin_id}`, `POST .../sessions/{id}/messages`, plus knowledge notes, playbooks, attachments and scheduled sessions.""",
    diagram="""sequenceDiagram
    participant C as Your code / another agent
    participant D as Devin
    C->>D: create session {prompt}
    D-->>C: devin_id
    D-->>C: blocked: question
    C->>D: message: answer
    D-->>C: finished + PR""",
    mapping=[("Client", "`DevinClient` (create, get, message, wait)")],
    live="export DEVIN_API_KEY=cog_... DEVIN_ORG_ID=...\npython -m services.s16_devin.devin --live",
    notes=["Because one HTTP call creates a session, any agent in this repo can hand coding work to Devin as a tool."])

S["s17_openai_codex"] = dict(
    title="17 - OpenAI Codex (Python SDK)", file="codex_agent.py",
    what="""OpenAI's coding agent. The Python SDK controls a local Codex app-server over JSON-RPC and ships a pinned runtime. Threads hold state; each turn can change the sandbox.""",
    api="""`pip install openai-codex`: `Codex()`, `thread_start(model, sandbox, approval_mode, cwd)`, `thread.run(prompt, sandbox=...)`, `result.final_response`. Sandboxes: `read_only`, `workspace_write`, `full_access`. Approval modes: `auto_review` (default), `deny_all`.""",
    diagram="""flowchart LR
    P[Turn 1: plan<br/>read_only] --> I[Turn 2: implement<br/>workspace_write]
    I --> R[Turn 3: review diff<br/>read_only]""",
    mapping=[("Per-turn sandbox", "the three-turn pattern in `run_live`")],
    live="pip install openai-codex\nexport OPENAI_API_KEY=...   # or sign in with ChatGPT\npython -m services.s17_openai_codex.codex_agent --live",
    notes=["Plan read-only, implement with write access, review read-only. Least privilege per turn costs nothing."])

S["s18_claude_agent_sdk"] = dict(
    title="18 - Claude Agent SDK (Anthropic)", file="claude_agent.py",
    what="""The Claude Code harness as a Python library. `query()` for one-shot runs, `ClaudeSDKClient` for multi-turn sessions with custom tools and hooks, `@tool` + `create_sdk_mcp_server` for in-process tools, `AgentDefinition` for subagents, `HookMatcher` for `PreToolUse`/`PostToolUse` hooks, and `ClaudeAgentOptions` for everything else (`allowed_tools`, `permission_mode`, `can_use_tool`, `max_turns`, `max_budget_usd`, `resume`, `skills`, `sandbox`...).""",
    api="""`pip install claude-agent-sdk` (Python 3.10+).""",
    diagram="""flowchart TB
    O[Orchestrator] -->|delegate| R[researcher<br/>AgentDefinition]
    O -->|delegate| W[writer<br/>AgentDefinition]
    O --> H{PreToolUse hook}
    H --> P{can_use_tool}
    P --> T[mcp__acme__send_email]""",
    mapping=[("Subagents", "`agents={'researcher': AgentDefinition(...), 'writer': ...}`"),
             ("Sentinel", "`PreToolUse` hook returning `permissionDecision: deny`"),
             ("Approval", "`can_use_tool` -> `PermissionResultAllow/Deny`"),
             ("Budget", "`max_budget_usd`, `max_turns`")],
    live="pip install claude-agent-sdk\nexport ANTHROPIC_API_KEY=...\npython -m services.s18_claude_agent_sdk.claude_agent --live",
    notes=["Hooks run before permission checks; use hooks for hard rules and `can_use_tool` for asking a person."])

S["s19_langchain_deep_agents"] = dict(
    title="19 - LangChain Deep Agents", file="deep_agent.py",
    what="""An opinionated harness on LangGraph: a virtual filesystem with pluggable backends, subagents through a task tool, summarization, skills and memory files, and human-in-the-loop interrupts. Model-agnostic. **Since 0.7 the `write_todos` planner is no longer in the default harness**; add `TodoListMiddleware()` if you want it. Much more in [frameworks/deep_agents](../../frameworks/deep_agents/README.md).""",
    api="""`create_deep_agent(model, tools, system_prompt, subagents=[{name, description, system_prompt, tools, model}], interrupt_on={...}, checkpointer=..., backend=..., skills=[...], memory=[...])`. Resume an interrupt with `Command(resume={"decisions": [{"type": "approve"}]})`.""",
    diagram="""flowchart LR
    U[User] --> A[Deep agent]
    A --> TD[write_todos]
    A --> FS[(virtual FS<br/>/memories/)]
    A -->|task| SA[researcher subagent]
    A --> I{interrupt_on<br/>send_email}
    I --> H((You))""",
    mapping=[("Todos", "`write_todos` tool (a pattern; opt-in via TodoListMiddleware in 0.7+)"),
             ("Virtual FS", "`SandboxComputer` as the filesystem; `/memories/` path"),
             ("Subagent", "`task` tool spawning a fresh agent"),
             ("interrupt_on", "approval on `send_email`; live code loops on `__interrupt__`")],
    live="pip install deepagents langgraph langchain-anthropic\nexport ANTHROPIC_API_KEY=...\npython -m services.s19_langchain_deep_agents.deep_agent --live",
    notes=["`interrupt_on` needs a checkpointer and a `thread_id` in the config; without them there's nothing to resume."])

S["s20_google_adk"] = dict(
    title="20 - Google Agent Development Kit (ADK)", file="adk_agent.py",
    what="""Google's framework for multi-agent systems: `Agent`/`LlmAgent`, workflow agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`), a `Runner` that yields Events, session services, shared `session.state` (an agent's `output_key` writes there), and before/after model and tool callbacks. Deploy with `adk web`, Cloud Run or Vertex AI Agent Engine. **ADK 2.0** (GA May 19 2026) turned ADK into a graph engine: `Workflow` with edges, routing, fan-out/join, retries, dynamic nodes and durable human-in-the-loop, and deprecated the classic Sequential/Parallel/Loop agents. See [frameworks/google_adk_workflows](../../frameworks/google_adk_workflows/README.md).""",
    api="""`pip install google-adk`; Gemini via `GOOGLE_API_KEY` or Vertex AI.""",
    diagram="""flowchart LR
    U[User] --> SEQ[SequentialAgent]
    SEQ --> F[finance_agent<br/>output_key=overdue]
    F --> ST[(session.state)]
    ST --> C["comms_agent<br/>instruction uses {overdue}"]
    C --> CB{before_tool_callback}
    CB --> E[send_email]""",
    mapping=[("output_key / state", "`state['overdue']` handed to the next agent"),
             ("before_tool_callback", "the comms agent's gate approves Northwind and skips BrightPath")],
    live="pip install google-adk\nexport GOOGLE_API_KEY=...\npython -m services.s20_google_adk.adk_agent --live",
    notes=["Returning a dict from `before_tool_callback` skips the real tool and hands that dict to the model as the result."])


def render(key: str, d: dict) -> str:
    rows = "\n".join(f"| {a} | {b} |" for a, b in d["mapping"])
    notes = "\n".join(f"- {n}" for n in d.get("notes", []))
    return f"""# {d['title']}

## What it is

{d['what']}

## What you can program

{d['api']}

## Architecture

```mermaid
{d['diagram']}
```

## How the example maps to it

| Concept | In `{d['file']}` |
|---|---|
{rows}

## Run it

```bash
# offline mock (no keys)
python -m services.{key}.{d['file'][:-3]}
```

```bash
# live
{d['live']}
```

## Notes

{notes}

Back to the [main README](../../README.md).
"""


if __name__ == "__main__":
    for key, d in S.items():
        (ROOT / key / "README.md").write_text(render(key, d))
    print(f"wrote {len(S)} service READMEs")
