"""Write a README.md into every use-case folder, plus usecases/swe_day/README.md.

    python usecases/swe_day/gen_readmes.py

The flow diagram in each README is built from the use case's plan, so it always matches
what the agent actually does in the offline run.
"""

from __future__ import annotations

import collections
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from usecases.swe_day import BLOCKS, all_usecases  # noqa: E402

FILE_TOOLS = {"write_file": "write", "read_file": "read", "edit_file": "edit", "ls": "ls", "grep": "grep", "glob": "glob"}
EFFECT_NOTE = {"read": "read-only", "write": "changes state", "external": "sends something outside", "money": "touches prod / money"}


def _clean(s: str, n: int = 48) -> str:
    s = re.sub(r"[\"<>{}\[\]|#;`]", "", str(s)).replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 3] + "..."


def _step_label(tc: dict, uc) -> tuple[str, str]:
    """(label, css class) for one tool call in the plan."""
    name, args = tc["name"], tc["args"]
    if name == "task":
        return f"subagent: {args.get('subagent_type', '')}", "sub"
    if name == "write_todos":
        return f"plan: {len(args.get('todos', []))} todos", "plan"
    if name in FILE_TOOLS:
        target = args.get("file_path") or args.get("path") or args.get("pattern") or ""
        return f"{FILE_TOOLS[name]} {_clean(target, 40)}", "file"
    if uc.output and name == uc.output[0]:
        return f"structured answer: {name}", "out"
    tags = []
    if name in uc.hitl:
        tags.append("needs approval")
    if name in uc.guard:
        tags.append("policy guard")
    return name + (f" ({', '.join(tags)})" if tags else ""), ("hitl" if name in uc.hitl else "guard" if name in uc.guard else "tool")


def mermaid_flow(uc) -> str:
    lines = ["flowchart TD", f'    T(["{_clean(uc.trigger, 50)}"]) --> A["Deep Agent"]']
    prev, k = ["A"], 0
    for msg in uc.plan:
        calls = msg.tool_calls or []
        if not calls:
            continue
        cur = []
        for tc in calls:
            k += 1
            label, cls = _step_label(tc, uc)
            nid = f"S{k}"
            lines.append(f'    {nid}["{label}"]:::{cls}')
            cur.append(nid)
        for p in prev:
            for c in cur:
                lines.append(f"    {p} --> {c}")
        prev = cur
    final = "typed result" if uc.output else "answer to you"
    lines.append(f'    Z(["{final}"])')
    for p in prev:
        lines.append(f"    {p} --> Z")
    lines += ["    classDef tool fill:#eef,stroke:#88a", "    classDef file fill:#efe,stroke:#8a8",
              "    classDef sub fill:#fef3dd,stroke:#c90", "    classDef plan fill:#f4f4f4,stroke:#999",
              "    classDef hitl fill:#fde,stroke:#c48", "    classDef guard fill:#fee,stroke:#c44",
              "    classDef out fill:#e8f6ff,stroke:#48c"]
    return "\n".join(lines)


def tools_table(uc) -> str:
    rows = ["| Tool | What it does | Effect | Control |", "|---|---|---|---|"]
    for t in uc.tools:
        ctl = []
        if t.name in uc.hitl:
            ctl.append("human approval")
        if t.name in uc.guard:
            ctl.append("policy guard")
        rows.append(f"| `{t.name}` | {t.desc} | {EFFECT_NOTE.get(t.effect, t.effect)} | {', '.join(ctl) or '-'} |")
    if not uc.tools:
        rows.append("| (none) | Only the built-in Deep Agents file tools | - | - |")
    return "\n".join(rows)


def production_notes(uc) -> list[str]:
    notes = []
    trig = uc.trigger.split(":", 1)
    kind, detail = trig[0].strip(), trig[1].strip() if len(trig) > 1 else ""
    if kind == "cron":
        notes.append(f"Schedule it with `{detail}` (cron, server time; prefix `CRON_TZ=...` for your zone). "
                     "A LangGraph Platform cron job, a GitHub Actions `schedule:`, or a Kubernetes CronJob all work.")
    elif kind == "webhook":
        notes.append(f"Start it from the `{detail}` webhook. A small FastAPI endpoint that calls "
                     "`agent.invoke(...)` with a fresh `thread_id` per event is enough.")
    elif kind == "slack":
        notes.append(f"Wire it to Slack ({detail}) with Slack Bolt; use the Slack thread id as the LangGraph `thread_id`.")
    else:
        notes.append("You start this one yourself: a CLI command, a Slack slash command or an IDE action.")
    if uc.hitl:
        notes.append("Approvals: the run pauses on an interrupt. In production, send the pending action to Slack or a web UI "
                     "and resume with `Command(resume={'decisions': [...]})` on the same `thread_id`. You need a persistent "
                     "checkpointer (Postgres) for this.")
    if uc.guard:
        notes.append("Keep the guard. It's ordinary Python in middleware, so it holds even when the model gets it wrong.")
    if uc.long_term_memory:
        notes.append("`/memories/` maps to a LangGraph store. Use `PostgresStore` so the next run (or tomorrow's) can read it.")
    if uc.subagents:
        notes.append("Subagents run in their own context window, which keeps the main thread small. Give them a cheaper model if the job is just reading.")
    if uc.output:
        notes.append(f"The `{uc.output[0]}` result is a Pydantic object, so you can post it straight to a dashboard or database.")
    notes.append("Swap each `TOOL(..., returns=...)` for a real call (your API, a CLI, or an MCP server through `langchain-mcp-adapters`).")
    return notes


def folder_readme(uc) -> str:
    rel = f"usecases/swe_day/{uc.folder}/usecase.py"
    parts = [
        f"# {uc.id:03d}. {uc.title}",
        "",
        f"**When:** {uc.time} ({uc.block})  ",
        f"**Trigger:** `{uc.trigger}`  ",
        f"**Type:** {uc.automation}  ",
        f"**Deep Agents features:** {', '.join(uc.features)}",
        "",
        uc.why,
        "",
        "## What you ask",
        "",
        f"> {uc.ask}",
        "",
        "## Flow",
        "",
        "```mermaid",
        mermaid_flow(uc),
        "```",
        "",
        "## Tools",
        "",
        tools_table(uc),
        "",
    ]
    if uc.subagents:
        parts += ["## Subagents", ""] + [f"- **{s.name}**: {s.desc} Tools: {', '.join(f'`{t}`' for t in s.tools) or 'none'}." for s in uc.subagents] + [""]
    if uc.skills:
        parts += ["## Skills", ""]
        for name, (desc, steps) in uc.skills.items():
            parts += [f"`/skills/{name}/SKILL.md`: {desc}", ""] + [f"{i}. {s}" for i, s in enumerate(steps, 1)] + [""]
    if uc.agents_md:
        parts += ["## House rules (AGENTS.md)", "", "```markdown", uc.agents_md.strip(), "```", ""]
    if uc.hitl:
        parts += ["## Human decisions in the offline run", ""]
        for tool, d in uc.hitl.items():
            parts.append(f"- `{tool}`: {_describe_decision(d)}")
        parts.append("")
    parts += [
        "## Run it",
        "",
        "```bash",
        f"python {rel}            # offline: scripted model, real Deep Agent",
        f"LC_MODEL=anthropic:claude-sonnet-4-6 python {rel} --live   # a real model makes the decisions",
        "```",
        "",
        "## Taking it to production",
        "",
    ] + [f"- {n}" for n in production_notes(uc)] + [""]
    return "\n".join(parts)


def _describe_decision(d) -> str:
    if isinstance(d, list):
        return "; ".join(f"call {i}: {_describe_decision(x)}" for i, x in enumerate(d, 1))
    if isinstance(d, tuple):
        return f"edited before running ({', '.join(d[1])})"
    return {"approve": "approved", "reject": "rejected"}.get(d, str(d))


DAY_INTRO = """# A software engineer's day on Deep Agents

100 use cases, one folder each, covering one backend engineer's day from 06:30 to midnight. The
engineer works on a payments platform (payments-api, ledger, checkout). Most of these jobs run on
their own: a cron schedule or a webhook starts them, and a person is pulled in only where a decision
needs one. The rest are things you'd ask for at your desk.

Every folder has a `usecase.py`, which is a real `deepagents.create_deep_agent(...)` run, and a
README with the flow, the tools, the controls and notes for production. Offline, a scripted model
makes the decisions, so everything runs in seconds with no API key. Add `--live` and a real model
drives the same agent.

```bash
pip install -r requirements-langchain.txt
python usecases/swe_day/run_day.py                    # the whole day, in time order (expect 100/100)
python usecases/swe_day/run_day.py --block ops        # one part of the day
python usecases/swe_day/run_day.py --id 49 -v         # one use case with its full trace
python usecases/swe_day/049_alert_to_incident_triage/usecase.py   # or run a folder directly
```

## How the day is split
"""

DAY_DESIGN = """
## How the automations are kept safe

The scripted model is fine for a demo, but these patterns are what keep you safe once a real model
is making the calls:

- **Read tools run freely.** Fetching CI logs, metrics or tickets has no side effects.
- **Writes that matter pause for a person** (`interrupt_on`). Merges, rollbacks, prod SQL, Slack posts
  and status-page updates wait for approve, edit or reject. The overnight jobs mostly avoid these, so they
  can run unattended.
- **Hard policy lives in code, not in the prompt** (`@wrap_tool_call` guards). Examples: no prod flag
  flips (#28), no scaling past the cap (#51), no Terraform apply that destroys something (#59), no
  deleting protected branches (#84) or audit logs (#87), no restore onto prod (#86), no secrets in PR
  comments (#45).
- **Evening runs leave notes for the morning ones.** `/memories/` is routed to a LangGraph store, so
  #79 (plan tomorrow) and #80 (save learnings) leave notes that later runs read.
- **Typed output where a machine reads the result.** Estimates, canary verdicts, cost and coverage
  reports come back as Pydantic objects (`response_format`).

## Running these for real

| Trigger in the README | What to use |
|---|---|
| `cron: ...` | LangGraph Platform cron jobs, GitHub Actions `schedule:`, a Kubernetes CronJob, or Cloud Scheduler hitting an endpoint |
| `webhook: ...` | A FastAPI endpoint per source (GitHub, Alertmanager, PagerDuty, Zendesk) that starts a run with a new `thread_id` |
| `slack: ...` | Slack Bolt; the Slack thread is the LangGraph thread, and approvals are buttons that resume the interrupt |
| `manual` | A CLI, a Slack slash command, or your IDE |

What you need in production:

1. A persistent checkpointer (`PostgresSaver`) so approvals can wait hours and survive restarts.
2. A persistent store (`PostgresStore`) behind `/memories/`.
3. Real tools in place of `TOOL(..., returns=...)`. Most of these map to an existing CLI or API (gh, kubectl,
   terraform, the Jira/Slack/PagerDuty APIs) or an MCP server.
4. Tracing (LangSmith or OpenTelemetry), so you can see why an overnight run did what it did.
5. Start the unattended jobs in report-only mode for a week before giving them write tools.

## Regenerating

Each `usecase.py` is the source of truth. If you edit one, or add a folder like `101_my_task/`, rebuild
the READMEs (flow diagrams included) from the code:

```bash
python usecases/swe_day/gen_readmes.py
```
"""


def day_readme(ucs) -> str:
    by_block = collections.defaultdict(list)
    for u in ucs:
        by_block[u.block].append(u)
    out = [DAY_INTRO, "```mermaid", "flowchart LR"]
    for i, (b, span, desc) in enumerate(BLOCKS):
        out.append(f'    B{i}["{span}<br/>{b}: {len(by_block[b])} use cases"]')
    out.append("    " + " --> ".join(f"B{i}" for i in range(len(BLOCKS))))
    out.append('    B6 -. "notes in /memories/" .-> B0')
    out += ["```", "", "| Block | Time | Use cases | What happens |", "|---|---|---|---|"]
    for b, span, desc in BLOCKS:
        items = by_block[b]
        out.append(f"| {b} | {span} | {items[0].id}-{items[-1].id} | {desc} |")
    trig = collections.Counter(u.trigger.split(":")[0] for u in ucs)
    feats = collections.Counter(f for u in ucs for f in u.features)
    out += ["", "How each one starts: " + ", ".join(f"{k} {v}" for k, v in trig.most_common()) + ".", "",
            "Deep Agents features used: " + ", ".join(f"{k} ({v})" for k, v in feats.most_common()) + "."]
    for b, span, desc in BLOCKS:
        out += ["", f"## {span} {b}", "", desc + ".", "",
                "| # | Time | Use case | Trigger | Type | Features |", "|---|---|---|---|---|---|"]
        for u in by_block[b]:
            out.append(f"| {u.id} | {u.time} | [{u.title}]({u.folder}/) | `{u.trigger}` | {u.automation} | {', '.join(u.features)} |")
    out.append(DAY_DESIGN)
    return "\n".join(out)


def main() -> None:
    ucs = all_usecases()
    for u in ucs:
        (HERE / u.folder / "README.md").write_text(folder_readme(u))
    (HERE / "README.md").write_text(day_readme(ucs))
    print(f"wrote {len(ucs)} folder READMEs and usecases/swe_day/README.md")


if __name__ == "__main__":
    main()
