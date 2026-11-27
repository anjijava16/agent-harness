"""Settings, all from environment variables (see .env.example)."""

from __future__ import annotations

import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

# sqlite:///./agent_app.db | postgresql+psycopg://user:pw@host/db | mysql+pymysql://user:pw@host/db
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{ROOT / 'agent_app.db'}")
# redis://localhost:6379/0 ; empty means an in-process fakeredis (fine for a laptop demo and tests)
REDIS_URL = os.environ.get("REDIS_URL", "")

FRAMEWORKS = ["deepagents", "langgraph", "adk", "claude"]
DEFAULT_FRAMEWORK = os.environ.get("DEFAULT_FRAMEWORK", "deepagents")
# scripted: the model's decisions come from the use case, no API key. live: a real model decides.
DEFAULT_MODE = os.environ.get("DEFAULT_MODE", "scripted")

LC_MODEL = os.environ.get("LC_MODEL", "anthropic:claude-sonnet-5-5")       # Deep Agents + LangGraph
ADK_MODEL = os.environ.get("ADK_MODEL", "gemini-2.5-flash")                  # Google ADK
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")           # Claude Agent SDK

RATE_LIMIT_PER_MIN = int(os.environ.get("RATE_LIMIT_PER_MIN", "120"))
TOOL_CACHE_TTL = int(os.environ.get("TOOL_CACHE_TTL", "300"))

# The person every use case is written for. Users override any of these in their preferences.
DEFAULT_PROFILE = {
    "name": "Sam Rivera",
    "home_city": "Chicago",
    "timezone": "America/Chicago",
    "work_hours": "09:00-17:30",
    "diet": "vegetarian",
    "partner": "Jordan",
    "kid": "Maya",
    "dog": "Biscuit",
    "currency": "USD",
    "max_purchase_without_review": 200,
    "monthly_grocery_budget": 600,
    "seat_preference": "aisle",
    "news_topics": "AI, climate, Chicago",
}
