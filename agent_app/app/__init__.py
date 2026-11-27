"""Personal agent app: UI -> FastAPI -> one of four agent runtimes, chosen per user.

Runtimes: LangChain Deep Agents, LangGraph, Google ADK, Claude Agent SDK.
Storage: SQLite, Postgres or MySQL through one DATABASE_URL. Redis for cache, rate limits,
locks and approval hand-off (fakeredis in-process when REDIS_URL isn't set).
"""
