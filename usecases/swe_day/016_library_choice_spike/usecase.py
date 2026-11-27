"""Library choice spike

When:     09:00 (planning)
Trigger:  manual
Type:     research

Two researcher subagents investigate in parallel; the main agent writes a short
recommendation.

Run:  python usecases/swe_day/016_library_choice_spike/usecase.py            (offline, scripted model)
      LC_MODEL=anthropic:claude-sonnet-4-6 python usecases/swe_day/016_library_choice_spike/usecase.py --live
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from usecases.engine import SUB, TOOL, UseCase, answer, call, edit, ls, par, read, run, say, task, todos, write  # noqa: E402,F401

TIME = "09:00"
BLOCK = "planning"
TRIGGER = "manual"
AUTOMATION = "research"

USECASE = UseCase(
    id=16,
    domain="swe-" + BLOCK,
    title="Library choice spike",
    ask="Should we use Celery or Arq for the new background jobs?",
    why="Two researcher subagents investigate in parallel; the main agent writes a short recommendation.",
    tools=[TOOL("package_stats", "Package health stats.", lambda pkg: {"celery": {"stars": 25000, "async": False, "last_release_days": 20},
                                                                       "arq": {"stars": 2300, "async": True, "last_release_days": 60}}[pkg], {"pkg": str})],
    subagents=[SUB("celery-scout", "Researches Celery.", ["package_stats"], [call("package_stats", pkg="celery"), say("Celery: mature, huge ecosystem, sync-first.")]),
               SUB("arq-scout", "Researches Arq.", ["package_stats"], [call("package_stats", pkg="arq"), say("Arq: async-native, small, fits FastAPI.")])],
    plan=[par(task("celery-scout", "Assess Celery for our FastAPI service"), task("arq-scout", "Assess Arq for our FastAPI service")),
          write("/spikes/background_jobs.md", "Recommend Arq: async-native, matches FastAPI. Celery if we need canvas/workflows later.\n"),
          say("Recommendation: Arq (async-native, fits FastAPI). Celery only if we need complex workflows. Spike notes saved.")]
)

if __name__ == "__main__":
    sys.exit(0 if run(USECASE, verbose=True).ok else 1)
