"""Run every service demo in mock mode, one after another, and print a summary table.

    python run_all.py            # full trace for every demo
    PA_QUIET=1 python run_all.py # just the summary
"""

from __future__ import annotations

import importlib
import time

SERVICES = [
    ("01", "Grok Bot (xAI)", "services.s01_grok_bot.grok_bot"),
    ("02", "dots (OpenAI)", "services.s02_openai_dots.dots"),
    ("03", "Claude Duet (Anthropic)", "services.s03_claude_duet.claude_duet"),
    ("04", "Gemini Task (Google)", "services.s04_gemini_task.gemini_task"),
    ("05", "Muse (Meta)", "services.s05_meta_muse.muse"),
    ("06", "Copilot Cowork (Microsoft)", "services.s06_copilot_cowork.copilot_cowork"),
    ("07", "Cue (Manus)", "services.s07_manus_cue.cue"),
    ("08", "OpenClaw (open source)", "services.s08_openclaw.openclaw"),
    ("09", "Instinct (Spear Street)", "services.s09_instinct.instinct"),
    ("10", "Personal Computer (Perplexity)", "services.s10_perplexity_personal_computer.personal_computer"),
    ("11", "Manus API", "services.s11_manus.manus"),
    ("12", "Hermes Agent (Nous)", "services.s12_hermes_agent.hermes"),
    ("13", "Genspark (MCP)", "services.s13_genspark.genspark"),
    ("14", "Comet (Perplexity)", "services.s14_perplexity_comet.comet"),
    ("15", "Cursor SDK", "services.s15_cursor.cursor_agent"),
    ("16", "Devin API", "services.s16_devin.devin"),
    ("17", "Codex SDK", "services.s17_openai_codex.codex_agent"),
    ("18", "Claude Agent SDK", "services.s18_claude_agent_sdk.claude_agent"),
    ("19", "LangChain Deep Agents", "services.s19_langchain_deep_agents.deep_agent"),
    ("20", "Google ADK", "services.s20_google_adk.adk_agent"),
]


def main() -> None:
    rows = []
    for num, label, mod in SERVICES:
        t0 = time.time()
        try:
            out = importlib.import_module(mod).run_mock()
            rows.append((num, label, "ok", f"{(time.time() - t0) * 1000:.0f} ms", str(out)[:70]))
        except Exception as e:  # keep going so one broken demo doesn't hide the rest
            rows.append((num, label, "FAIL", "-", f"{type(e).__name__}: {e}"[:70]))
    print("\n" + "-" * 120)
    for r in rows:
        print(f"{r[0]}  {r[1]:<32} {r[2]:<5} {r[3]:>7}  {r[4]}")
    print("-" * 120)
    if any(r[2] != "ok" for r in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
