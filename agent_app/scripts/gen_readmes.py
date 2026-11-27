"""Write README.md into every use-case folder, plus usecases/README.md (the catalogue).

    python scripts/gen_readmes.py

Flow diagrams are built from each use case's steps, so they always match what runs.
"""

from __future__ import annotations

import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import config  # noqa: E402
from app.usecases import AREAS, UC_DIR, all_usecases  # noqa: E402

EFFECT = {"read": "read-only", "write": "changes your data", "external": "talks to someone else", "money": "spends money"}


def _clean(s: str, n: int = 44) -> str:
    s = re.sub(r"[\"<>{}\[\]|#;`]", "", str(s)).replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 3] + "..."


def _label(uc, name: str, args: dict) -> tuple[str, str]:  # noqa: ANN001
    if name == "remember":
        return f"remember {_clean(args.get('key', ''), 30)}", "mem"
    if name == "recall":
        return f"recall {_clean(args.get('topic', ''), 30)}", "mem"
    tags = (["approval"] if name in uc.gated else []) + (["guard"] if name in uc.guards else [])
    cls = "appr" if name in uc.gated else "guard" if name in uc.guards else "tool"
    return name + (f" - {', '.join(tags)}" if tags else ""), cls


def flow(uc) -> str:  # noqa: ANN001
    lines = ["flowchart TD", '    U(["You, in the UI"]) --> API["FastAPI"] --> RT["Your framework:<br/>Deep Agents, LangGraph, ADK or Claude SDK"]']
    prev, k = ["RT"], 0
    for s in uc.steps:
        if not s.calls:
            continue
        cur = []
        for name, args in s.calls:
            k += 1
            label, cls = _label(uc, name, args)
            lines.append(f'    S{k}["{label}"]:::{cls}')
            cur.append(f"S{k}")
        lines += [f"    {p} --> {c}" for p in prev for c in cur]
        prev = cur
    lines.append('    Z(["Answer"])')
    lines += [f"    {p} --> Z" for p in prev]
    lines += ["    classDef tool fill:#eef,stroke:#88a", "    classDef mem fill:#efe,stroke:#8a8",
              "    classDef appr fill:#fde,stroke:#c48", "    classDef guard fill:#fee,stroke:#c44"]
    return "\n".join(lines)


def _decision(d) -> str:  # noqa: ANN001
    if isinstance(d, list):
        return "; ".join(f"call {i}: {_decision(x)}" for i, x in enumerate(d, 1))
    if isinstance(d, tuple):
        return "approve with edits " + ", ".join(f"`{k}={v!r}`" for k, v in d[1].items())
    return d


def folder_readme(uc) -> str:  # noqa: ANN001
    rel = f"usecases/{uc.folder}/usecase.py"
    used = sorted({k for s in uc.steps for _, a in s.calls for v in a.values() if isinstance(v, str) for k in re.findall(r"\{([a-z_]+)\}", v)}
                  | set(re.findall(r"\{([a-z_]+)\}", uc.ask + " ".join(s.text or "" for s in uc.steps))))
    out = [f"# {uc.id:03d}. {uc.title}", "",
           f"**Area:** {dict(AREAS)[uc.area]}  ", f"**Features:** {', '.join(uc.features) or 'tools only'}", "",
           uc.why, "", "## What you ask", "", f"> {uc.ask}", "", "## Flow", "", "```mermaid", flow(uc), "```", "",
           "## Tools", "", "| Tool | Effect | Control |", "|---|---|---|"]
    for t in uc.tools:
        ctl = ", ".join((["approval"] if t.name in uc.gated else []) + (["guard"] if t.name in uc.guards else [])) or "-"
        out.append(f"| `{t.name}`: {t.desc} | {EFFECT[t.effect]} | {ctl} |")
    if not uc.tools:
        out.append("| (only `remember` / `recall`) | memory | - |")
    out.append("")
    if uc.approvals:
        out += ["## Approvals", "", "In the UI the run pauses and you decide. With auto-approve (demo), these decisions are used:", ""]
        out += [f"- `{tool}`: {_decision(d)}" for tool, d in uc.approvals.items()] + [""]
    if uc.guards:
        out += ["## Guards", "", "Checked in the shared tool layer before the tool runs, the same on every framework. "
                "Guards get your preferences, so changing a limit in the UI changes what's allowed.", ""]
        out += [f"- `{tool}`" for tool in uc.guards] + [""]
    if used:
        prof = config.DEFAULT_PROFILE
        out += ["## Preferences it uses", "", "| Preference | Default |", "|---|---|"]
        out += [f"| `{k}` | {prof.get(k, uc.prefs.get(k, '-'))} |" for k in used] + [""]
    out += ["## Run it", "", "```bash", f"python {rel}                 # your preferred framework",
            f"python {rel} --all           # all four frameworks", f"python {rel} --manual        # answer the approvals yourself",
            f"python {rel} --framework adk --live   # Gemini decides (needs GOOGLE_API_KEY)", "```", "",
            "Or start the app (`uvicorn app.api:app`), open http://localhost:8000 and pick it from the list.", ""]
    return "\n".join(out)


def catalogue(ucs) -> str:  # noqa: ANN001
    feats = collections.Counter(f for u in ucs for f in u.features)
    out = ["# 200 use cases for one person", "",
           "Everything Sam Rivera might hand to a personal agent in a year, from the morning brief to filing taxes. "
           "Each folder has a `usecase.py` (a framework-neutral spec) and a README with the flow. The same spec runs on "
           "LangChain Deep Agents, LangGraph, Google ADK or the Claude Agent SDK, whichever the user picked.", "",
           "Features used: " + ", ".join(f"{k} ({v})" for k, v in feats.most_common()) + ".", ""]
    by = collections.defaultdict(list)
    for u in ucs:
        by[u.area].append(u)
    for area, label in AREAS:
        items = by[area]
        out += [f"## {label} ({items[0].id}-{items[-1].id})", "", "| # | Use case | You ask | Features |", "|---|---|---|---|"]
        out += [f"| {u.id} | [{u.title}]({u.folder}/) | {u.ask} | {', '.join(u.features)} |" for u in items] + [""]
    return "\n".join(out)


def main() -> None:
    ucs = all_usecases()
    for u in ucs:
        (UC_DIR / u.folder / "README.md").write_text(folder_readme(u))
    (UC_DIR / "README.md").write_text(catalogue(ucs))
    print(f"wrote {len(ucs)} READMEs and usecases/README.md")


if __name__ == "__main__":
    main()
