"""Order-tracking tables. They sit on the same SQLAlchemy Base and DATABASE_URL as the rest of
agent_app, so SQLite, Postgres and MySQL all work with no changes."""

from __future__ import annotations

import datetime as dt

from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, Integer, String, Text, delete
from sqlalchemy.orm import Mapped, mapped_column

from app import db
from app.db import Base, _now


class Order(Base):
    __tablename__ = "ot_orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    customer: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200))
    items: Mapped[str] = mapped_column(String(300))
    total: Mapped[float] = mapped_column(Float)
    carrier: Mapped[str] = mapped_column(String(20))
    tracking_no: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(30), default="created")
    promised: Mapped[dt.date] = mapped_column(Date)
    eta: Mapped[dt.date] = mapped_column(Date)
    scenario: Mapped[str] = mapped_column(String(20))       # which path the simulator plays
    step: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now, onupdate=_now)


class TrackingEvent(Base):
    __tablename__ = "ot_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("ot_orders.id"), index=True)
    code: Mapped[str] = mapped_column(String(30))
    detail: Mapped[str] = mapped_column(String(300))
    location: Mapped[str] = mapped_column(String(100))
    at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)


class Notification(Base):
    __tablename__ = "ot_notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, index=True)
    kind: Mapped[str] = mapped_column(String(30))
    message: Mapped[str] = mapped_column(Text)
    by: Mapped[str] = mapped_column(String(60))
    at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)


class Ticket(Base):
    __tablename__ = "ot_tickets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, index=True)
    reason: Mapped[str] = mapped_column(String(200))
    priority: Mapped[str] = mapped_column(String(10))
    status: Mapped[str] = mapped_column(String(20), default="open")
    by: Mapped[str] = mapped_column(String(60))
    at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)


class Approval(Base):
    """Risky actions (credits, reships) never run straight from an agent. They wait here for a person."""
    __tablename__ = "ot_approvals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, index=True)
    action: Mapped[str] = mapped_column(String(20))         # credit | reship
    args: Mapped[dict] = mapped_column(JSON)
    reason: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(20), default="pending")   # pending | approved | rejected
    by: Mapped[str] = mapped_column(String(60))
    decided_by: Mapped[str] = mapped_column(String(60), default="")
    at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)


class AgentRun(Base):
    __tablename__ = "ot_agent_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agent_type: Mapped[str] = mapped_column(String(20))
    runtime: Mapped[str] = mapped_column(String(20))
    mode: Mapped[str] = mapped_column(String(20))
    trigger: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20), default="running")
    summary: Mapped[str] = mapped_column(Text, default="")
    path: Mapped[list] = mapped_column(JSON, default=list)  # graph agents: nodes visited
    started: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)
    finished: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)


class AgentStep(Base):
    __tablename__ = "ot_agent_steps"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(Integer, index=True)
    kind: Mapped[str] = mapped_column(String(20))           # tool | node | iteration
    name: Mapped[str] = mapped_column(String(60))
    args: Mapped[dict] = mapped_column(JSON, default=dict)
    result: Mapped[object] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="ok")
    at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)


TABLES = [AgentStep, AgentRun, Approval, Ticket, Notification, TrackingEvent, Order]


def ensure() -> None:
    with db.session():
        pass
    Base.metadata.create_all(db._engine, tables=[t.__table__ for t in TABLES])


def wipe() -> None:
    ensure()
    with db.session() as s:
        for t in TABLES:
            s.execute(delete(t))
