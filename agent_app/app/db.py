"""SQLAlchemy models. The same code runs on SQLite, Postgres and MySQL; only DATABASE_URL changes."""

from __future__ import annotations

import datetime as dt
import uuid
from contextlib import contextmanager

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from . import config


def _now() -> dt.datetime:
    return dt.datetime.now(dt.UTC).replace(tzinfo=None)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), default="")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)


class Preference(Base):
    __tablename__ = "preferences"
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), primary_key=True)
    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[object] = mapped_column(JSON)


class Run(Base):
    __tablename__ = "runs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), index=True)
    usecase_id: Mapped[int] = mapped_column(Integer)
    framework: Mapped[str] = mapped_column(String(20))
    mode: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(30), default="running")   # running | awaiting_approval | done | error
    ask: Mapped[str] = mapped_column(Text, default="")
    final: Mapped[str] = mapped_column(Text, default="")
    pending: Mapped[list] = mapped_column(JSON, default=list)
    checks: Mapped[list] = mapped_column(JSON, default=list)
    error: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now, onupdate=_now)


class ToolCall(Base):
    __tablename__ = "tool_calls"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("runs.id"), index=True)
    tool: Mapped[str] = mapped_column(String(100))
    args: Mapped[dict] = mapped_column(JSON)
    result: Mapped[object] = mapped_column(JSON, nullable=True)
    effect: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20))   # ok | cached | blocked | rejected
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("runs.id"), index=True)
    kind: Mapped[str] = mapped_column(String(30))
    data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)


class Memory(Base):
    """Long-term memory per user, shared by every framework (the remember / recall tools)."""
    __tablename__ = "memories"
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), primary_key=True)
    key: Mapped[str] = mapped_column(String(200), primary_key=True)
    value: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now, onupdate=_now)


_engine = None
_Session = None


def init(url: str | None = None) -> None:
    """Create the engine and tables. Safe to call again with a new URL (tests do)."""
    global _engine, _Session
    url = url or config.DATABASE_URL
    kw = {"connect_args": {"check_same_thread": False}} if url.startswith("sqlite") else {"pool_pre_ping": True}
    _engine = create_engine(url, **kw)
    _Session = sessionmaker(_engine, expire_on_commit=False)
    Base.metadata.create_all(_engine)


def dialect() -> str:
    if _engine is None:
        init()
    return _engine.dialect.name


@contextmanager
def session():
    if _Session is None:
        init()
    s = _Session()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def ensure_user(user_id: str, name: str = "") -> None:
    with session() as s:
        if s.get(User, user_id) is None:
            s.add(User(id=user_id, name=name or user_id))


def get_prefs(user_id: str) -> dict:
    with session() as s:
        return {p.key: p.value for p in s.scalars(select(Preference).where(Preference.user_id == user_id))}


def set_prefs(user_id: str, values: dict) -> None:
    ensure_user(user_id)
    with session() as s:
        for k, v in values.items():
            row = s.get(Preference, (user_id, k))
            if row is None:
                s.add(Preference(user_id=user_id, key=k, value=v))
            else:
                row.value = v


def add_event(run_id: str, kind: str, data: dict) -> None:
    with session() as s:
        s.add(Event(run_id=run_id, kind=kind, data=data))
