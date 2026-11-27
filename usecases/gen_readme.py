"""Regenerate usecases/README.md from the catalogue (python usecases/gen_readme.py)."""

from __future__ import annotations

import collections
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from usecases.catalog import all_usecases  # noqa: E402

INTRO = """# 100 use cases on the Deep Agents harness (LangChain)

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
"""


def main() -> None:
    ucs = all_usecases()
    feats = collections.Counter(f for u in ucs for f in u.features)
    lines = [INTRO, "## Feature coverage\n", "| Feature | Use cases |", "|---|---|"]
    lines += [f"| {f} | {n} |" for f, n in feats.most_common()]
    by_domain = collections.defaultdict(list)
    for u in ucs:
        by_domain[u.domain].append(u)
    lines.append("\n## The catalogue\n")
    for dom, items in by_domain.items():
        lines.append(f"\n### {dom} ({items[0].id}-{items[-1].id})\n")
        lines.append("| # | Use case | What the user asks | Why it suits an agent | Deep Agents features |")
        lines.append("|---|---|---|---|---|")
        for u in items:
            lines.append(f"| {u.id} | **{u.title}** | {u.ask} | {u.why} | {', '.join(u.features)} |")
    (HERE / "README.md").write_text("\n".join(lines) + "\n")
    print(f"wrote usecases/README.md ({len(ucs)} use cases)")


if __name__ == "__main__":
    main()
