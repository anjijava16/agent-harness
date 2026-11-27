"""The canonical "morning ops" plan, as the scripted model would produce it.

Live models will produce their own plan from MORNING_GOAL; this script is what a good
plan looks like, and it lets every mock demo run deterministically.
"""

from __future__ import annotations

from .llm import Step

REMINDER = ("Hi {name}, a friendly nudge that invoice {inv} for ${amt:,.2f} is now {days} days past due. "
            "You can pay here: https://pay.acme.studio/{inv}. Happy to resend it if that helps. Thanks! - Acme Studio")


def morning_script(channel: str = "#ops", send: bool = True, include_focus: bool = True) -> list[Step]:
    steps = [
        Step.call("read_inbox", "Start with what's new in the inbox."),
        Step.call("list_overdue_invoices", "Two emails mention invoices; check the ledger.", min_days=1),
        Step.call("web_search", "Check tone guidance for reminders.", query="late payment reminder etiquette"),
        Step.call("draft_email", "Draft for Northwind (14 days).", to="ap@northwind.com",
                  subject="Reminder: INV-1038", body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
        Step.call("draft_email", "Draft for BrightPath (3 days, they asked for a resend).", to="maria@brightpath.io",
                  subject="INV-1042 (resent)", body=REMINDER.format(name="Maria", inv="INV-1042", amt=850, days=3)),
    ]
    if send:
        steps += [
            Step.call("send_email", "Send Northwind reminder.", to="ap@northwind.com", subject="Reminder: INV-1038",
                      body=REMINDER.format(name="Northwind team", inv="INV-1038", amt=2400, days=14)),
            Step.call("send_email", "Send BrightPath resend.", to="maria@brightpath.io", subject="INV-1042 (resent)",
                      body=REMINDER.format(name="Maria", inv="INV-1042", amt=850, days=3)),
        ]
    if include_focus:
        steps.append(Step.call("add_focus_block", "Protect Tuesday morning.", day="Tue", start="09:00", end="11:00",
                               title="Focus"))
    steps += [
        Step.call("post_message", "Tell the team.", channel=channel,
                  text="Morning ops: 2 overdue invoices ($3,250 total), reminders drafted"
                       + (" and sent" if send else "") + ". Focus block Tue 9-11."),
        Step.final("Morning ops done: reminders drafted, sent where you approved, focus block added, team updated."),
    ]
    return steps
