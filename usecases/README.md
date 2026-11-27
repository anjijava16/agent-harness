# 100 use cases on the Deep Agents harness (LangChain)

Every use case is a real `deepagents.create_deep_agent(...)` run: real tools, real subagents through the
`task` tool, real filesystem backends, real human-in-the-loop interrupts, real middleware. Offline, only
the model's decisions are scripted, so all 100 run in a few seconds with no API key and are checked
automatically. With `--live`, a real model drives exactly the same agent.

Checked with `deepagents 0.7.42`, `langchain 1.5.2`, `langgraph 1.2.24`.

```bash
pip install -r requirements-langchain.txt          # Python 3.11+
python usecases/run.py --list                       # the catalogue
python usecases/run.py 22                           # one use case with a full trace
python usecases/run.py --domain finance             # a whole domain
python usecases/run.py --all                        # all 100 + checks (expect 100/100)
LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/run.py 22 --live   # a real model; approvals asked in the terminal
```

> **Also here:** [swe_day/](swe_day/README.md) has 100 more, one folder each, covering a software
> engineer's day from 06:30 to midnight (cron and webhook automations, code review, incidents, releases,
> overnight jobs). Run them with `python usecases/swe_day/run_day.py`.

## How a use case is defined

A use case is data, not a script. `usecases/engine.py` turns it into a Deep Agent:

```python
UseCase(22, "support", "Refund request handling",
    ask="Handle ticket #4411: customer wants a refund for a late delivery.",
    why="Policy lookup + refund; refunds need a supervisor, and the amount is edited down.",
    tools=[TOOL("get_order", "Fetch an order.", {...}, {"order_id": str}),
           TOOL("issue_refund", "Refund an order.", "refunded", {"order_id": str, "amount": float}, effect="money")],
    skills={"refund-policy": ("Use for any refund.", ["Late > 5 days: refund shipping + 20%", ...])},
    plan=[read("/skills/refund-policy/SKILL.md"),            # what the scripted model decides, step by step
          call("get_order", order_id="O-77"),
          call("issue_refund", order_id="O-77", amount=240.0),
          say("Refund issued at the approved amount ...")],
    hitl={"issue_refund": ("edit", {"amount": 48.0})},       # the human edits the refund to $48
    expect=[("refund edited", lambda c: c["world"].actions[0]["args"]["amount"] == 48.0)])
```

| Spec field | Becomes in Deep Agents |
|---|---|
| `tools=[TOOL(...)]` | LangChain `StructuredTool`s (canned data offline; replace `returns=` with a real API call) |
| `subagents=[SUB(...)]` | `subagents=[{"name", "description", "system_prompt", "tools", "model"}]`, reached via `task` |
| `plan=[...]` | the scripted model's turns: `call`, `par` (parallel calls), `task`, `write`/`read`/`edit`/`ls`, `todos`, `answer`, `say` |
| `hitl={tool: decision}` | `interrupt_on={tool: {"allowed_decisions": [...]}}` + checkpointer; decisions `approve`, `reject`, `("edit", {...})` or a list (one per call) |
| `guard={tool: fn}` | a `@wrap_tool_call` middleware that blocks deterministically (fn can see this run's history) |
| `skills={...}` / `agents_md=` / `seed_files=` | a real temp folder via `FilesystemBackend`, `skills=["/skills/"]`, `memory=["/AGENTS.md"]` |
| `long_term_memory=True` | `CompositeBackend(routes={"/memories/": StoreBackend(...)})` + `InMemoryStore` |
| `todos(...)` in the plan | `TodoListMiddleware()` (not in the default harness since 0.7) |
| `output=(Name, fields)` | `response_format=ToolStrategy(PydanticModel)` -> `result["structured_response"]` |
| `expect=[...]` | checks on what actually happened: tool calls, side effects, blocks, files, store keys, structured output |

Every run also checks automatically that each planned tool actually ran (or was blocked or rejected on purpose) and that the final answer was delivered.

## From example to production

1. Replace each `TOOL(..., returns=...)` with a function that calls your real system (or MCP tools via `langchain-mcp-adapters`).
2. Drop `plan=`. With `--live` (or `LC_MODEL`), the model makes its own decisions and approvals for every non-read tool go to a person.
3. Swap `MemorySaver`/`InMemoryStore` for Postgres or SQLite checkpointers and stores.
4. Keep `guard=` rules. They're the part that holds when the model is wrong.

## Feature coverage

| Feature | Use cases |
|---|---|
| filesystem | 47 |
| parallel calls | 44 |
| HITL | 28 |
| subagents | 20 |
| structured output | 16 |
| guardrail | 9 |
| todos | 8 |
| long-term memory | 8 |
| AGENTS.md | 7 |
| skills | 6 |

## The catalogue


### finance (1-10)

| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |
|---|---|---|---|---|
| 1 | **AR collections run** | Chase every invoice more than 7 days overdue. | Repetitive, rule-bound, but each email needs judgment on tone; sending must be approved. | HITL, filesystem, parallel calls |
| 2 | **Three-way invoice match (AP)** | Match this week's vendor invoices against POs and receipts; hold anything that doesn't match. | Classic AP control. The agent does the matching; a guardrail stops payment of unmatched invoices. | guardrail, parallel calls |
| 3 | **Expense report audit** | Audit November expense reports against policy and flag violations. | Policy lives in a skill file, so finance can change rules without touching code. | skills, filesystem |
| 4 | **Month-end close checklist** | Run the month-end close for November. | Long, ordered, multi-step work: the todo list gives a visible plan you can follow. | HITL, todos, parallel calls |
| 5 | **Budget vs actual variance memo** | Explain the big Q4 budget variances for the CFO. | A researcher subagent pulls numbers; the main agent writes the narrative. | subagents, filesystem |
| 6 | **13-week cash forecast** | Update the 13-week cash forecast and tell me the lowest week. | Structured output so the result feeds straight into a dashboard. | parallel calls, structured output |
| 7 | **Vendor onboarding with KYC** | Onboard Brightline Logistics as a vendor. | Mixes lookups, a sanctions check and a bank-detail change that must be human-approved. | HITL, parallel calls |
| 8 | **Payroll pre-run sanity check** | Sanity-check this payroll run before it goes out. | Anomaly spotting is judgment; the agent never runs payroll itself (no such tool). | parallel calls |
| 9 | **Tax document collection** | Collect 1099 info from contractors who haven't sent W-9s. | Outreach from a template, and progress remembered across sessions in /memories/. | long-term memory, filesystem, parallel calls |
| 10 | **Card fraud alert triage** | Triage today's card fraud alerts. | Fan out one analysis per alert; freezing a card is approval-gated and one alert is a false positive. | HITL, parallel calls |

### engineering (11-20)

| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |
|---|---|---|---|---|
| 11 | **Bug report triage** | Triage the new GitHub issues from last night. | Label, dedupe and prioritize; filing labels is a write, so it's guarded to known labels only. | guardrail, parallel calls |
| 12 | **Pull request review** | Review PR #88 (adds invoice reminders job). | A reviewer subagent reads the diff; the main agent posts one consolidated review after approval. | subagents, HITL, parallel calls |
| 13 | **Dependency upgrade plan** | Plan the upgrade off the deprecated requests-oauthlib version. | Reads the repo's real files, writes a plan; nothing is changed without a human. | filesystem |
| 14 | **Flaky test investigation** | Find out why test_checkout is flaky. | Pulls run history, finds the pattern, and edits a real file to quarantine the test. | filesystem |
| 15 | **Incident postmortem draft** | Draft the postmortem for yesterday's checkout outage. | Parallel evidence gathering from logs, alerts and the incident channel, then a blameless write-up. | filesystem, parallel calls |
| 16 | **Release notes from merged PRs** | Write release notes for v2.32. | Classic summarization with a house style kept in AGENTS.md. | AGENTS.md, filesystem |
| 17 | **API documentation generator** | Document the /invoices endpoints for the developer portal. | Reads source, produces structured docs; output is typed so the portal can render it. | structured output |
| 18 | **Security vulnerability triage** | Triage this week's scanner findings. | Prioritizes by exploitability; creating tickets is fine, but auto-closing findings is rejected by a human. | HITL |
| 19 | **Production log analysis** | Why did 5xx errors spike at 09:00? | A log-analyst subagent keeps the huge log output out of the main agent's context. | subagents |
| 20 | **Database migration plan** | Plan moving the invoices table to partitioned storage. | Big, risky change: todo plan, a DBA subagent, and the plan saved for review. | subagents, todos, filesystem |

### support (21-30)

| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |
|---|---|---|---|---|
| 21 | **Ticket triage to queues** | Route the unassigned support tickets. | Structured output per batch, so routing code can trust the shape. | structured output |
| 22 | **Refund request handling** | Handle ticket #4411: customer wants a refund for a late delivery. | Policy lookup + refund; refunds over $100 need a supervisor, and the amount is edited down. | HITL, skills, filesystem |
| 23 | **Knowledge-base answer with citations** | Answer: how do I export invoices to CSV? | Search, read, answer with the article link; no guessing. |  |
| 24 | **Escalation to engineering** | Ticket #4502 says the API returns 500 on every invoice create. Escalate properly. | Reproduces, collects evidence, files one well-formed bug instead of a forwarded email. |  |
| 25 | **Churn-risk outreach** | Reach out to accounts showing churn risk this week. | A scoring subagent picks accounts; outreach emails are approved one by one (one rejected). | subagents, HITL, parallel calls |
| 26 | **SLA breach watch** | Which tickets will breach SLA in the next 2 hours? | Simple but valuable: computes deadlines, reassigns, and remembers who is overloaded. | long-term memory, filesystem |
| 27 | **Multilingual reply** | Reply to the Spanish-language ticket #6120 about a double charge. | Translation is just another step; tone rules live in AGENTS.md. | HITL, AGENTS.md |
| 28 | **Warranty claim intake** | Process the warranty claim emailed in by Ravi Shah. | Extracts fields from a messy email into a typed claim. | structured output |
| 29 | **Order status lookup** | Where is order O-5510? | The everyday case: two lookups, one honest answer. |  |
| 30 | **CSAT theme analysis** | What are customers unhappy about this month? | Fan out over survey batches with a subagent, then write a themes report. | subagents, filesystem |

### sales-marketing (31-40)

| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |
|---|---|---|---|---|
| 31 | **Inbound lead research** | Research the 3 new inbound leads and score them. | Parallel enrichment, then a typed score your CRM can ingest. | parallel calls, structured output |
| 32 | **Account brief before a call** | Brief me on Globex before tomorrow's 10am call. | Research subagent + CRM history, one page you can read in two minutes. | subagents, filesystem, parallel calls |
| 33 | **Personalized outbound sequence** | Draft a 3-email sequence for the CFO persona. | Brand voice in a skill; drafts land as files for the team to edit. | skills, filesystem |
| 34 | **Competitor watch** | What did our top 3 competitors ship this month? | Weekly-style monitoring; findings appended to long-term memory so next month can diff. | long-term memory, filesystem, parallel calls |
| 35 | **Campaign performance report** | How did the November webinar campaign do? | Pulls from two systems and explains it in plain English. | parallel calls |
| 36 | **SEO content brief** | Write an SEO brief for 'how to reduce days sales outstanding'. | Keyword data + SERP research by a subagent; brief has a fixed structure. | subagents, filesystem, parallel calls |
| 37 | **Social post calendar** | Plan next week's LinkedIn posts. | Scheduling is a write that a human approves; one post gets edited. | HITL, AGENTS.md, todos, parallel calls |
| 38 | **CRM hygiene** | Clean up duplicate contacts in the CRM. | Finds duplicates; merges are destructive, so the guardrail caps a run at 2 merges. | guardrail |
| 39 | **Proposal draft from a template** | Draft the Globex proposal from our template. | Reads a real template file, fills it, writes the proposal next to it. | filesystem |
| 40 | **Event follow-up** | Follow up with everyone who visited our booth at FinOps Summit. | Batch personalization from scanned badges; sending is approval-gated as one batch. | HITL, parallel calls |

### research (41-50)

| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |
|---|---|---|---|---|
| 41 | **Literature review** | Review recent work on agent harness design. | The canonical deep-agent task: plan, delegate searches, keep notes, synthesize. | subagents, todos, filesystem |
| 42 | **Market sizing** | Size the US market for SMB accounts-receivable automation. | Bottom-up math with sources; result is typed for the deck. | parallel calls, structured output |
| 43 | **Due-diligence memo** | Do first-pass diligence on acquiring Ledgr. | Three specialist subagents in parallel (financials, product, legal), one memo. | subagents, filesystem, parallel calls |
| 44 | **Daily news digest** | Give me today's digest on AR automation and payments. | Scheduled-style task; digest format fixed in AGENTS.md. | AGENTS.md, parallel calls |
| 45 | **Patent landscape scan** | Any patents that could block our auto-reminder feature? | Search + careful reading by a subagent; the conclusion is written to a file for counsel. | subagents, filesystem |
| 46 | **Survey analysis** | Analyze the 400 responses to the pricing survey. | Numbers by tool, narrative by model, results typed. | structured output |
| 47 | **Fact-check a draft** | Fact-check the blog draft before it goes live. | Reads the draft, checks each claim, edits the wrong number in place. | filesystem |
| 48 | **Meeting notes to action items** | Turn the board meeting transcript into action items with owners. | Extraction into a strict schema. | structured output |
| 49 | **Knowledge base curation** | Find stale help articles and propose updates. | Long-term memory of what was reviewed, so the next run skips it. | long-term memory, filesystem |
| 50 | **Policy comparison** | Compare our data-retention policy with the new EU guidance. | Reads two documents from the filesystem and writes a gap table. | filesystem |

### data (51-60)

| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |
|---|---|---|---|---|
| 51 | **Natural-language SQL report** | What was revenue by region last quarter? | Read-only SQL; a guardrail rejects anything that isn't a SELECT. | guardrail |
| 52 | **Data quality check** | Check the customers table for quality issues. | Runs checks in parallel and writes a report the data team can track. | filesystem, parallel calls |
| 53 | **KPI anomaly explanation** | Signups dropped 30% yesterday. Why? | Breaks the metric down by dimension with a subagent and finds the culprit. | subagents |
| 54 | **A/B test readout** | Read out the pricing-page A/B test. | Stats computed by a tool, decision typed, so nobody eyeballs p-values. | structured output |
| 55 | **Dashboard spec from a question** | I want a dashboard for collections health. | Turns a vague ask into a concrete spec file with metrics and queries. | filesystem |
| 56 | **ETL failure triage** | The nightly payments ETL failed. Fix or escalate. | Reads the error, retries once (allowed), escalates if it fails again. |  |
| 57 | **Cohort retention analysis** | How does retention differ for customers who used reminders in month 1? | Two cohorts via SQL, insight in one sentence, chart spec saved. | filesystem, parallel calls |
| 58 | **Revenue forecast** | Forecast next quarter's revenue. | A modeling subagent does the math; the answer comes back typed with a range. | subagents, structured output |
| 59 | **Schema documentation** | Document the payments schema for new analysts. | Reads metadata, writes docs; house conventions from AGENTS.md. | AGENTS.md, filesystem |
| 60 | **PII scan across tables** | Scan the warehouse for unmasked PII. | Parallel scans; anything found is written to a restricted report, never echoed in chat. | filesystem, parallel calls |

### hr (61-70)

| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |
|---|---|---|---|---|
| 61 | **Resume screening against a rubric** | Screen the 3 applicants for the Senior Data Engineer role. | Rubric in a skill; scores are typed; a guardrail blocks use of protected attributes. | guardrail, skills, filesystem, structured output |
| 62 | **Interview scheduling** | Schedule A1's onsite with 3 interviewers next week. | Calendar intersection across people; invites need approval. | HITL, parallel calls |
| 63 | **New-hire onboarding plan** | Build a 30-day onboarding plan for Priya (Account Exec, starts Monday). | Todo-driven plan from a template file; tasks created in the HR system. | filesystem, parallel calls |
| 64 | **HR policy Q&A** | How many days of parental leave do I get? | Answers only from the handbook file, with the section cited. | filesystem |
| 65 | **Offer letter with approval** | Draft and send Priya's offer: $96k base. | Compensation changes go through a human; the salary is edited before sending. | HITL |
| 66 | **Performance review prep** | Prepare my notes for Sam's review. | Pulls goals and feedback via a subagent; manager-only notes stay in the filesystem. | subagents, filesystem |
| 67 | **PTO conflict check** | Can I approve Lee's PTO for Dec 22-31? | Checks team coverage rules before suggesting an answer. | parallel calls |
| 68 | **Job description writer** | Write the JD for a Staff Platform Engineer. | Uses an inclusive-language skill and writes the JD file. | skills, filesystem |
| 69 | **Exit interview themes** | What themes come up in this year's exit interviews? | Aggregates text, returns typed themes; individual comments stay private. | structured output |
| 70 | **Training plan from skill gaps** | Build a Q1 training plan for the support team. | Gap analysis subagent + plan; remembered for the next quarter. | subagents, long-term memory, filesystem |

### ops-it (71-80)

| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |
|---|---|---|---|---|
| 71 | **Access request with least privilege** | Give Priya access to the finance dashboards. | Grants only what the role needs; admin-level grants are blocked by policy. | guardrail |
| 72 | **Laptop provisioning** | Provision a laptop for Priya starting Monday. | Multi-system checklist with a todo list; the purchase is approval-gated. | HITL, todos |
| 73 | **On-call handoff summary** | Write the on-call handoff for the next shift. | Summarizes alerts and open incidents into the standard format. | AGENTS.md, filesystem, parallel calls |
| 74 | **Cloud cost optimization** | Find savings in our AWS bill. | A FinOps subagent analyzes; deleting resources is rejected by a human, rightsizing approved. | subagents, HITL, parallel calls |
| 75 | **Backup verification** | Verify last night's backups actually restore. | Restore tests in parallel; results in a typed report for auditors. | parallel calls, structured output |
| 76 | **Inventory reorder** | Reorder anything below safety stock. | Purchases have a budget cap enforced in code. | guardrail, parallel calls |
| 77 | **Shipping exception handling** | Handle today's shipping exceptions. | Per-exception decisions, with customer notices approved before sending. | HITL, parallel calls |
| 78 | **Vendor SLA review** | Did our vendors meet their SLAs last quarter? | Compares contract terms (files) with measured uptime (tool). | filesystem, parallel calls |
| 79 | **Change request review** | Review CR-301 (DB failover test Saturday) for risk. | Checks the change calendar and runbook; writes a risk note; approves nothing itself. | filesystem |
| 80 | **Phishing report triage** | Triage the emails users reported as phishing today. | Analysis subagent; quarantine needs approval; one report is a false positive. | subagents, HITL |

### legal (81-90)

| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |
|---|---|---|---|---|
| 81 | **Contract clause review** | Review the Globex MSA against our playbook. | Playbook as a skill; findings typed so legal ops can track them. | skills, filesystem, structured output |
| 82 | **NDA triage** | Can we sign the NDA from Initech as is? | High-volume, low-risk: auto-clear standard NDAs, route anything unusual. | filesystem |
| 83 | **GDPR data subject access request** | Process DSAR from maria@brightpath.io. | Finds personal data across systems in parallel; the export is sent only after approval. | HITL, todos, parallel calls |
| 84 | **Policy gap analysis vs SOC 2** | Where do our policies fall short of SOC 2? | A compliance subagent maps controls; gaps saved for the audit tracker. | subagents, filesystem |
| 85 | **Audit evidence collection** | Collect Q4 access-review evidence for the auditors. | Gathers screenshots/exports into a folder with an index; long, so it has a todo list. | todos, filesystem, parallel calls |
| 86 | **Sanctions screening** | Screen this week's new customers against sanctions lists. | Possible hits are frozen only with approval; clean ones pass. | HITL, parallel calls |
| 87 | **Regulatory change watch** | Any new regulations affecting invoicing this month? | Monitoring with memory of what's already been reported. | long-term memory, filesystem |
| 88 | **Contract renewal tracker** | Which vendor contracts auto-renew in the next 60 days? | Structured list for a renewal calendar. | structured output |
| 89 | **Open-source license check** | Are any of our dependencies' licenses a problem for a SaaS product? | Reads the dependency manifest; flags copyleft-network licenses. | filesystem, parallel calls |
| 90 | **Security incident disclosure draft** | Draft the customer notice for the API key leak. | Drafting is fine; publishing is rejected until legal signs off. | HITL, AGENTS.md, filesystem |

### personal (91-100)

| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |
|---|---|---|---|---|
| 91 | **Morning brief** | Give me my morning brief. | The flagship personal-agent task: read-only checks in parallel, one short brief. | parallel calls |
| 92 | **Trip planning on a budget** | Plan my trip to the AI conference in Austin, Dec 9-11, under $1,200. | Research by subagent, booking approval-gated, hotel edited to a cheaper option. | subagents, HITL, parallel calls |
| 93 | **Inbox zero pass** | Get my inbox under control. | Archives and labels freely; anything that replies to a person asks first. | HITL |
| 94 | **Bill pay with approval** | Pay this month's bills. | Money moves only with approval, and a spending cap blocks the unexpected one. | HITL, guardrail, parallel calls |
| 95 | **Meal plan and grocery order** | Plan dinners for the week and order groceries. I'm vegetarian. | Preferences from memory, plan as a file, order approval-gated. | HITL, long-term memory, filesystem |
| 96 | **Calendar defrag** | Give me two 2-hour focus blocks this week. | Finds gaps, moves one movable meeting with approval. | HITL, parallel calls |
| 97 | **Home maintenance scheduler** | Keep track of house maintenance and book what's due. | Recurring tasks remembered; booking a contractor needs a yes. | HITL, long-term memory, filesystem |
| 98 | **Personal learning plan** | Make me a 6-week plan to learn Google ADK 2.0 workflows. | A research subagent finds material; the plan is a todo list you can track. | subagents, todos |
| 99 | **Gift planning** | Help me get holiday gifts for my team of 5, about $50 each. | Preferences per person from memory files; purchase capped and approved. | HITL, guardrail, filesystem, parallel calls |
| 100 | **Subscription audit** | Find subscriptions I'm not using and cancel them. | Pulls card charges and usage; each cancellation is a separate approval (one kept). | HITL, parallel calls, structured output |
