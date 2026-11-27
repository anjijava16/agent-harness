"""A small engine that turns a declarative use-case spec into a real Deep Agents run.

Every one of the 100 use cases is a `UseCase(...)`. The engine:

  1. builds LangChain tools from TOOL specs (canned data offline; swap for real APIs),
  2. builds subagents with their own scripted models,
  3. picks a backend (state, real folder with seeded skills/AGENTS.md, /memories/ store),
  4. adds middleware the spec asks for (todos, guardrails, audit),
  5. calls deepagents.create_deep_agent(...) and runs it, resolving human-in-the-loop
     interrupts with the decisions the spec scripts,
  6. checks the outcome (every planned step ran, final answer, spec-specific expectations).

Offline the model's turns are scripted (`plan=`), so the run is deterministic and free.
With --live, a real model (LC_MODEL) drives the same agent, tools, subagents and policies,
and approvals are asked on the terminal.
"""

from __future__ import annotations

import itertools
import json
import os
import pathlib
import sys
import tempfile
import warnings
from dataclasses import dataclass, field
from typing import Any, Callable

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

from deepagents import create_deep_agent  # noqa: E402
from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend, StoreBackend  # noqa: E402
from langchain.agents.middleware import TodoListMiddleware, wrap_tool_call  # noqa: E402
from langchain.agents.structured_output import ToolStrategy  # noqa: E402
from langchain_core.messages import AIMessage, ToolMessage  # noqa: E402
from langchain_core.tools import StructuredTool  # noqa: E402
from langgraph.checkpoint.memory import MemorySaver  # noqa: E402
from langgraph.store.memory import InMemoryStore  # noqa: E402
from langgraph.types import Command  # noqa: E402
from pydantic import create_model  # noqa: E402

from frameworks._fakes.lc_fake import ScriptedChatModel  # noqa: E402

# =========================================================================================
# Spec DSL
# =========================================================================================

_ids = itertools.count(1)


@dataclass
class TOOL:
    """A tool the agent can call.

    name/desc   what the model sees
    args        {"arg": type} (default {"query": str})
    returns     canned data, or a callable(**args) -> data
    effect      "read" | "write" | "external" | "money"  (non-read calls are recorded as actions)
    """
    name: str
    desc: str
    returns: Any = "ok"
    args: dict = field(default_factory=lambda: {"query": str})
    effect: str = "read"


@dataclass
class SUB:
    """A subagent reached through Deep Agents' `task` tool."""
    name: str
    desc: str
    tools: list[str]
    script: list            # steps for the subagent's own scripted model (call/par/say)
    prompt: str = ""


# ---- plan steps (what the scripted model "decides") -------------------------------------

def call(name: str, /, **args) -> AIMessage:  # noqa: ANN003
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": f"c{next(_ids)}"}])


def par(*steps: AIMessage) -> AIMessage:
    """Several tool calls in one model turn (run in parallel by the harness)."""
    return AIMessage(content="", tool_calls=[tc for s in steps for tc in s.tool_calls])


def task(subagent: str, description: str) -> AIMessage:
    return call("task", description=description, subagent_type=subagent)


def write(path: str, content: str) -> AIMessage:
    return call("write_file", file_path=path, content=content)


def read(path: str) -> AIMessage:
    return call("read_file", file_path=path)


def edit(path: str, old: str, new: str) -> AIMessage:
    return call("edit_file", file_path=path, old_string=old, new_string=new)


def ls(path: str = "/") -> AIMessage:
    return call("ls", path=path)


def todos(*items: str, done: int = 0) -> AIMessage:
    rows = [{"content": c, "status": "completed" if i < done else ("in_progress" if i == done else "pending")}
            for i, c in enumerate(items)]
    return call("write_todos", todos=rows)


def say(text: str) -> AIMessage:
    return AIMessage(content=text)


def answer(schema_name: str, /, **fields) -> AIMessage:  # noqa: ANN003
    """Final structured answer (response_format). Name must match UseCase.output name."""
    return call(schema_name, **fields)


@dataclass
class UseCase:
    id: int
    domain: str
    title: str
    ask: str                                   # what the user types
    why: str                                   # one line: what makes it a good agent task
    tools: list[TOOL]
    plan: list[AIMessage]
    subagents: list[SUB] = field(default_factory=list)
    hitl: dict = field(default_factory=dict)   # tool -> "approve" | "reject" | ("edit", {args}) | [one per call]
    guard: dict = field(default_factory=dict)  # tool -> callable(args[, world]) -> reason | None  (block if reason)
    skills: dict = field(default_factory=dict) # skill-name -> (description, [steps])
    agents_md: str = ""                        # house rules (memory=["/AGENTS.md"])
    seed_files: dict = field(default_factory=dict)  # path -> content in the agent's filesystem
    long_term_memory: bool = False             # route /memories/ to a persistent store
    output: tuple | None = None                # (SchemaName, {field: type}) -> response_format
    expect: list = field(default_factory=list) # [(label, callable(ctx) -> bool)]

    @property
    def features(self) -> list[str]:
        f = []
        names = {tc["name"] for m in self.plan for tc in (m.tool_calls or [])}
        if self.subagents:
            f.append("subagents")
        if self.hitl:
            f.append("HITL")
        if self.guard:
            f.append("guardrail")
        if self.skills:
            f.append("skills")
        if self.agents_md:
            f.append("AGENTS.md")
        if self.long_term_memory:
            f.append("long-term memory")
        if "write_todos" in names:
            f.append("todos")
        if names & {"write_file", "edit_file", "read_file", "ls"}:
            f.append("filesystem")
        if any(len(m.tool_calls or []) > 1 for m in self.plan):
            f.append("parallel calls")
        if self.output:
            f.append("structured output")
        return f


# =========================================================================================
# Build + run
# =========================================================================================


@dataclass
class World:
    calls: list = field(default_factory=list)      # every tool call that executed
    actions: list = field(default_factory=list)    # side-effecting calls (write/external/money)
    blocked: list = field(default_factory=list)    # guardrail blocks
    rejected: list = field(default_factory=list)   # human rejections
    approvals: list = field(default_factory=list)  # (tool, decision)


def _make_tool(spec: TOOL, world: World) -> StructuredTool:
    def fn(**kw):  # noqa: ANN003, ANN202
        world.calls.append((spec.name, kw))
        if spec.effect != "read":
            world.actions.append({"tool": spec.name, "effect": spec.effect, "args": kw})
        out = spec.returns(**kw) if callable(spec.returns) else spec.returns
        return out if isinstance(out, str) else json.dumps(out, default=str)

    schema = create_model(f"{spec.name}_args", **{k: (t, ...) for k, t in spec.args.items()})
    return StructuredTool.from_function(func=fn, name=spec.name, description=spec.desc, args_schema=schema)


def _model(script: list):  # noqa: ANN202
    if "--live" in sys.argv:
        from langchain.chat_models import init_chat_model

        return init_chat_model(os.environ.get("LC_MODEL", "anthropic:claude-sonnet-4-6"))
    return ScriptedChatModel(messages=iter(list(script)))


@dataclass
class Result:
    uc: UseCase
    ok: bool
    checks: list
    final: str
    world: World
    files: dict
    store_keys: list
    structured: Any
    error: str = ""


def build(uc: UseCase):  # noqa: ANN201
    world = World()
    tools = {t.name: _make_tool(t, world) for t in uc.tools}

    subagents = [{
        "name": s.name, "description": s.desc,
        "system_prompt": s.prompt or f"You are the {s.name} specialist. {s.desc} Be concise and factual.",
        "tools": [tools[n] for n in s.tools], "model": _model(s.script),
    } for s in uc.subagents]

    middleware: list = []
    if any(tc["name"] == "write_todos" for m in uc.plan for tc in (m.tool_calls or [])) or "--live" in sys.argv:
        middleware.append(TodoListMiddleware())
    if uc.guard:
        @wrap_tool_call
        def guardrail(request, handler):  # noqa: ANN001, ANN202
            check = uc.guard.get(request.tool_call["name"])
            if check is None:
                reason = None
            elif check.__code__.co_argcount >= 2:      # guard can look at what already happened this run
                reason = check(request.tool_call["args"], world)
            else:
                reason = check(request.tool_call["args"])
            if reason:
                world.blocked.append((request.tool_call["name"], reason))
                return ToolMessage(content=f"BLOCKED by policy: {reason}", tool_call_id=request.tool_call["id"],
                                   name=request.tool_call["name"])
            return handler(request)
        middleware.append(guardrail)

    # Backend: real temp folder when we need seeded files; /memories/ routed to a store if asked.
    tmp = None
    store = InMemoryStore() if uc.long_term_memory else None
    kwargs: dict = {}
    if uc.skills or uc.agents_md or uc.seed_files:
        tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"uc{uc.id:03d}_"))
        for name, (desc, steps) in uc.skills.items():
            d = tmp / "skills" / name
            d.mkdir(parents=True)
            body = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
            (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {desc}\n---\n\n{body}\n")
        if uc.agents_md:
            (tmp / "AGENTS.md").write_text(uc.agents_md)
        for path, content in uc.seed_files.items():
            p = tmp / path.lstrip("/")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
        base = FilesystemBackend(root_dir=tmp, virtual_mode=True)
        if uc.skills:
            kwargs["skills"] = ["/skills/"]
        if uc.agents_md:
            kwargs["memory"] = ["/AGENTS.md"]
    else:
        base = StateBackend()
    if store is not None:
        base = CompositeBackend(default=base, routes={
            "/memories/": StoreBackend(namespace=lambda rt: ("usecases", "memories"), store=store)})
        kwargs["store"] = store

    interrupt_on = {t: {"allowed_decisions": ["approve", "edit", "reject"]} for t in uc.hitl}
    if "--live" in sys.argv:   # in live mode, anything with side effects asks you
        interrupt_on.update({t.name: {"allowed_decisions": ["approve", "edit", "reject"]}
                             for t in uc.tools if t.effect != "read"})
    response_format = None
    if uc.output:
        name, fields = uc.output
        response_format = ToolStrategy(create_model(name, **{k: (v, ...) for k, v in fields.items()}))

    agent = create_deep_agent(
        model=_model(uc.plan),
        tools=list(tools.values()),
        system_prompt=f"You are a {uc.domain} agent. Job: {uc.title}. {uc.why}",
        subagents=subagents or None,
        middleware=middleware,
        backend=base,
        interrupt_on=interrupt_on or None,
        checkpointer=MemorySaver() if interrupt_on else None,
        response_format=response_format,
        **kwargs,
    )
    return agent, world, tmp, store


def _decide(uc: UseCase, action: dict, world: World) -> dict:
    name = action["name"]
    if "--live" in sys.argv:
        yes = input(f"\n[approve?] {name}({json.dumps(action['args'])[:200]}) [y/N] ").lower().startswith("y")
        choice = "approve" if yes else "reject"
    else:
        choice = uc.hitl.get(name, "approve")
        if isinstance(choice, list):                       # one decision per call, in order
            n = sum(1 for a in world.approvals if a[0] == name)
            choice = choice[n] if n < len(choice) else choice[-1]
    world.approvals.append((name, choice if isinstance(choice, str) else choice[0]))
    if choice == "approve":
        return {"type": "approve"}
    if choice == "reject":
        world.rejected.append(name)
        return {"type": "reject", "message": f"The user declined {name}."}
    _, new_args = choice
    return {"type": "edit", "edited_action": {"name": name, "args": {**action["args"], **new_args}}}


def run(uc: UseCase, verbose: bool = False) -> Result:
    agent, world, tmp, store = build(uc)
    cfg = {"configurable": {"thread_id": f"uc-{uc.id}"}, "recursion_limit": 80}
    try:
        r = agent.invoke({"messages": [{"role": "user", "content": uc.ask}]}, cfg)
        while r.get("__interrupt__"):
            req = r["__interrupt__"][0].value
            r = agent.invoke(Command(resume={"decisions": [_decide(uc, a, world) for a in req["action_requests"]]}), cfg)
    except Exception as e:  # noqa: BLE001
        return Result(uc, False, [("ran without error", False)], "", world, {}, [], None, f"{type(e).__name__}: {e}")

    files: dict = {}
    if tmp:
        files = {"/" + str(p.relative_to(tmp)): p.read_text() for p in tmp.rglob("*") if p.is_file()}
    for path, fd in (r.get("files") or {}).items():
        files[path] = "\n".join(fd.get("content", [])) if isinstance(fd, dict) and isinstance(fd.get("content"), list) \
            else (fd.get("content") if isinstance(fd, dict) else str(fd))
    store_keys = [i.key for i in store.search(("usecases", "memories"))] if store else []
    final = r["messages"][-1].content if isinstance(r["messages"][-1].content, str) else str(r["messages"][-1].content)
    structured = r.get("structured_response")

    checks = []
    if "--live" not in sys.argv:
        planned = [tc["name"] for m in uc.plan for tc in (m.tool_calls or [])
                   if tc["name"] not in {"task", "write_todos", "write_file", "read_file", "edit_file", "ls", "grep", "glob"}
                   and (not uc.output or tc["name"] != uc.output[0])]
        executed = [c[0] for c in world.calls]
        missing = [n for n in planned if n not in executed and n not in world.rejected
                   and n not in [b[0] for b in world.blocked]]
        checks.append(("every planned tool ran (or was blocked/rejected on purpose)", not missing))
        last_say = next((m.content for m in reversed(uc.plan) if m.content), None)
        if uc.output:
            checks.append(("structured output produced", structured is not None))
        elif last_say:
            checks.append(("final answer delivered", final == last_say))
    ctx = {"world": world, "files": files, "store_keys": store_keys, "final": final, "structured": structured, "result": r}
    for label, fn in uc.expect:
        try:
            checks.append((label, bool(fn(ctx))))
        except Exception:  # noqa: BLE001
            checks.append((label, False))
    ok = all(c[1] for c in checks)
    if verbose:
        _print(uc, r, world, files, store_keys, structured, checks)
    return Result(uc, ok, checks, final, world, files, store_keys, structured)


def _print(uc, r, world, files, store_keys, structured, checks) -> None:  # noqa: ANN001
    print(f"\n#{uc.id:03d} [{uc.domain}] {uc.title}")
    print(f"  user: {uc.ask}")
    print(f"  features: {', '.join(uc.features)}")
    for m in r["messages"][1:]:
        if getattr(m, "tool_calls", None):
            for tc in m.tool_calls:
                print(f"    -> {tc['name']}({json.dumps(tc['args'])[:110]})")
        elif m.type == "tool":
            print(f"    <- {m.name}: {str(m.content)[:110]}")
        elif m.content:
            print(f"    ai: {str(m.content)[:160]}")
    if world.approvals:
        print(f"  approvals: {world.approvals}")
    if world.blocked:
        print(f"  blocked: {world.blocked}")
    if files:
        print(f"  files: {sorted(files)}")
    if store_keys:
        print(f"  long-term memory keys: {store_keys}")
    if structured is not None:
        print(f"  structured: {structured!r}"[:220])
    for label, ok in checks:
        print(f"  [{'pass' if ok else 'FAIL'}] {label}")
