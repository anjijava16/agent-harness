"""Tiny shared CLI so every example runs the same way:

    python -m services.s01_grok_bot.grok_bot            # offline mock (default)
    python -m services.s01_grok_bot.grok_bot --live     # real SDK / API, needs keys
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Callable


def load_dotenv_if_present() -> None:
    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv()
    except ImportError:
        pass


def require_env(*names: str) -> None:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        sys.exit(f"Missing environment variables for live mode: {', '.join(missing)}. "
                 f"Copy .env.example to .env and fill them in, or run without --live.")


def main(mock: Callable[[], object], live: Callable[[], object] | None = None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="call the real service (needs API keys)")
    args = ap.parse_args()
    load_dotenv_if_present()
    if args.live:
        if live is None:
            sys.exit("This service has no public programmable API; only the mock/build-alike runs.")
        live()
    else:
        out = mock()
        if out is not None:
            print("\nresult:", out)
