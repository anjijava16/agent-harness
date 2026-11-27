"""A fake but realistic workspace that every demo shares.

The scenario is the same across all 20 examples so you can compare them side by side:

    "Acme Studio" is a two-person design shop. Every morning someone has to:
      1. skim the inbox,
      2. spot overdue invoices,
      3. draft (and, with approval, send) payment reminders,
      4. protect a focus block on the calendar,
      5. post a short status note to the team channel.

Connectors here stand in for Gmail / Outlook, Google Calendar, Stripe, Slack / Teams.
Real products reach these through OAuth connectors or MCP servers; the agent loop
doesn't care which, it only sees tools.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field

from .tools import Risk, Tool, tool

SEED_INBOX = [
    {"id": "m1", "from": "maria@brightpath.io", "subject": "Re: Invoice INV-1042",
     "body": "Hi! Sorry, this slipped. Can you resend the invoice?", "unread": True},
    {"id": "m2", "from": "noreply@stripe.com", "subject": "Invoice INV-1038 is 14 days overdue",
     "body": "Customer: Northwind Ltd. Amount: $2,400.00", "unread": True},
    {"id": "m3", "from": "sam@acme.studio", "subject": "Lunch Thursday?",
     "body": "Thai place again?", "unread": True},
    {"id": "m4", "from": "events@pyconf.org", "subject": "Speaker confirmation: Dec 9",
     "body": "Confirming your talk on Wednesday, Dec 9 at 2pm.", "unread": False},
]

SEED_INVOICES = [
    {"id": "INV-1038", "customer": "Northwind Ltd", "email": "ap@northwind.com",
     "amount": 2400.00, "days_overdue": 14, "status": "open"},
    {"id": "INV-1042", "customer": "BrightPath", "email": "maria@brightpath.io",
     "amount": 850.00, "days_overdue": 3, "status": "open"},
    {"id": "INV-1044", "customer": "Contoso", "email": "pay@contoso.com",
     "amount": 1200.00, "days_overdue": 0, "status": "paid"},
]

SEED_CALENDAR = [
    {"title": "Client call - Northwind", "day": "Mon", "start": "10:00", "end": "10:30"},
    {"title": "PyConf talk", "day": "Tue", "start": "14:00", "end": "15:00"},
]

WEB = {
    "late payment reminder etiquette": "Be friendly, restate amount and due date, include a pay link, "
                                       "offer to resend. Escalate tone only after 30 days.",
    "northwind ltd": "Northwind Ltd: UK wholesale distributor, AP handled by ap@northwind.com.",
}


@dataclass
class Workspace:
    inbox: list[dict] = field(default_factory=lambda: copy.deepcopy(SEED_INBOX))
    invoices: list[dict] = field(default_factory=lambda: copy.deepcopy(SEED_INVOICES))
    calendar: list[dict] = field(default_factory=lambda: copy.deepcopy(SEED_CALENDAR))
    drafts: list[dict] = field(default_factory=list)
    sent: list[dict] = field(default_factory=list)
    channel: list[dict] = field(default_factory=list)
    payments: list[dict] = field(default_factory=list)
    owner_domain: str = "acme.studio"

    # ---- tools -----------------------------------------------------------------------
    def tools(self) -> list[Tool]:
        ws = self

        @tool(risk=Risk.READ)
        def read_inbox(only_unread: bool = True) -> list:
            """List inbox messages (id, from, subject, body)."""
            return [m for m in ws.inbox if m["unread"] or not only_unread]

        @tool(risk=Risk.READ)
        def list_overdue_invoices(min_days: int = 1) -> list:
            """List open invoices that are at least min_days overdue."""
            return [i for i in ws.invoices if i["status"] == "open" and i["days_overdue"] >= min_days]

        @tool(risk=Risk.READ)
        def read_calendar(day: str = "") -> list:
            """List calendar events, optionally for one day (Mon..Sun)."""
            return [e for e in ws.calendar if not day or e["day"] == day]

        @tool(risk=Risk.READ)
        def web_search(query: str) -> str:
            """Search the web (canned results in mock mode)."""
            for k, v in WEB.items():
                if k in query.lower():
                    return v
            return "No strong results."

        @tool(risk=Risk.WRITE)
        def draft_email(to: str, subject: str, body: str) -> dict:
            """Save an email draft. Nothing is sent."""
            d = {"id": f"d{len(ws.drafts) + 1}", "to": to, "subject": subject, "body": body}
            ws.drafts.append(d)
            return d

        @tool(risk=Risk.EXTERNAL)
        def send_email(to: str, subject: str, body: str) -> dict:
            """Send an email to someone outside the agent. Visible to other people."""
            m = {"to": to, "subject": subject, "body": body}
            ws.sent.append(m)
            return {"status": "sent", **m}

        @tool(risk=Risk.WRITE)
        def add_focus_block(day: str, start: str, end: str, title: str = "Focus") -> dict:
            """Add a private focus block to your own calendar."""
            for e in ws.calendar:
                if e["day"] == day and not (end <= e["start"] or start >= e["end"]):
                    return {"status": "conflict", "with": e["title"]}
            ev = {"title": title, "day": day, "start": start, "end": end}
            ws.calendar.append(ev)
            return {"status": "added", **ev}

        @tool(risk=Risk.EXTERNAL)
        def post_message(channel: str, text: str) -> dict:
            """Post a message to a team chat channel (Slack/Teams/WhatsApp)."""
            ws.channel.append({"channel": channel, "text": text})
            return {"status": "posted", "channel": channel}

        @tool(risk=Risk.MONEY)
        def pay(merchant: str, amount: float, memo: str = "") -> dict:
            """Pay a merchant. Spends real money."""
            p = {"merchant": merchant, "amount": amount, "memo": memo}
            ws.payments.append(p)
            return {"status": "paid", **p}

        return [read_inbox, list_overdue_invoices, read_calendar, web_search, draft_email,
                send_email, add_focus_block, post_message, pay]

    # ---- assertions for tests ----------------------------------------------------------
    def summary(self) -> dict:
        return {"drafts": len(self.drafts), "sent": len(self.sent), "posts": len(self.channel),
                "payments": len(self.payments),
                "focus_blocks": sum(1 for e in self.calendar if e["title"].startswith("Focus"))}


MORNING_GOAL = (
    "Morning ops for Acme Studio: check the inbox, find overdue invoices, draft a friendly "
    "reminder for each, send them if I approve, add a 2-hour focus block on Tuesday morning, "
    "and post a short status note to #ops."
)
