"""A carrier simulator that produces tracking scans over time.

Each order follows a scenario (normal, delayed, weather, address, lost, damaged). Every tick,
each order still in transit moves one step with some probability. The seeded RNG makes a run
repeatable: tests replay exactly, and the UI gets something that looks live.
"""

from __future__ import annotations

import datetime as dt
import random

from sqlalchemy import select

from app import db

from . import bus
from .models import Order, TrackingEvent, ensure, wipe

SCENARIOS = {
    "normal": ["label_created", "picked_up", "in_transit", "in_transit", "out_for_delivery", "delivered"],
    "delayed": ["label_created", "picked_up", "in_transit", "delayed", "in_transit", "out_for_delivery", "delivered"],
    "weather": ["label_created", "picked_up", "weather_hold", "in_transit", "out_for_delivery", "delivered"],
    "address": ["label_created", "picked_up", "in_transit", "out_for_delivery", "address_issue", "out_for_delivery", "delivered"],
    "lost": ["label_created", "picked_up", "in_transit", "lost"],
    "damaged": ["label_created", "picked_up", "in_transit", "out_for_delivery", "damaged"],
}
STATUS = {"label_created": "label_created", "picked_up": "picked_up", "in_transit": "in_transit", "delayed": "delayed",
          "weather_hold": "delayed", "out_for_delivery": "out_for_delivery", "address_issue": "exception",
          "lost": "lost", "damaged": "damaged", "delivered": "delivered"}
DETAIL = {"label_created": "Shipping label created", "picked_up": "Picked up by carrier", "in_transit": "Arrived at sort facility",
          "delayed": "Running late: missed connection at hub", "weather_hold": "Held at facility due to winter storm",
          "out_for_delivery": "Out for delivery", "address_issue": "Delivery attempted: address incomplete (no apartment number)",
          "lost": "Carrier reports package cannot be located", "damaged": "Package damaged in transit; contents broken",
          "delivered": "Delivered, left at front door"}
PLACES = ["Joliet, IL", "Indianapolis, IN", "Columbus, OH", "Memphis, TN", "Louisville, KY", "Chicago, IL"]
CUSTOMERS = [("Ana Lopez", "Wireless earbuds", 89.0), ("Ben Okafor", "Standing desk", 420.0), ("Chloe Park", "Running shoes", 130.0),
             ("Dev Mehta", "Coffee grinder", 149.0), ("Erin Walsh", "Winter jacket", 210.0), ("Femi Ade", "Board game bundle", 64.0),
             ("Grace Liu", "Ceramic plates (set of 8)", 96.0), ("Hugo Brandt", "Monitor arm", 75.0), ("Iris Novak", "Yoga mat", 42.0),
             ("Jon Reyes", "Espresso cups", 38.0), ("Kim Sato", "Desk lamp", 58.0), ("Leo Grant", "Backpack", 110.0)]
PLAN = ["normal", "delayed", "lost", "address", "weather", "damaged", "normal", "delayed", "normal", "normal", "damaged", "normal"]
CARRIERS = ["ups", "fedex", "usps"]


class Simulator:
    def __init__(self, seed: int = 7, move_chance: float = 0.65):
        self.rng = random.Random(seed)
        self.move_chance = move_chance

    def reset(self, n: int = 12) -> list[int]:
        """Fresh orders, no events. Clears the order-tracking tables and Redis keys."""
        wipe()
        bus.wipe()
        today = dt.date.today()
        ids = []
        with db.session() as s:
            for i in range(n):
                name, item, total = CUSTOMERS[i % len(CUSTOMERS)]
                oid = 1001 + i
                s.add(Order(id=oid, customer=name, email=name.split()[0].lower() + "@example.com", items=item, total=total,
                            carrier=CARRIERS[i % 3], tracking_no=f"1Z{oid}{i:03d}", status="created",
                            promised=today + dt.timedelta(days=3), eta=today + dt.timedelta(days=3), scenario=PLAN[i % len(PLAN)]))
                ids.append(oid)
        return ids

    def tick(self) -> list[dict]:
        """Advance the world one step. Returns the new events (also written to DB and Redis)."""
        ensure()
        out = []
        with db.session() as s:
            for o in s.scalars(select(Order).order_by(Order.id)).all():
                path = SCENARIOS[o.scenario]
                if o.step >= len(path) or self.rng.random() > self.move_chance:
                    continue
                code = path[o.step]
                o.step += 1
                o.status = STATUS[code]
                if code in ("delayed", "weather_hold"):
                    o.eta = o.eta + dt.timedelta(days=2)
                ev = TrackingEvent(order_id=o.id, code=code, detail=DETAIL[code], location=self.rng.choice(PLACES))
                s.add(ev)
                s.flush()
                out.append({"event_id": ev.id, "order_id": o.id, "code": code, "detail": ev.detail, "location": ev.location,
                            "status": o.status, "carrier": o.carrier})
        for e in out:
            bus.publish_event(e)
        return out

    def done(self) -> bool:
        with db.session() as s:
            return all(o.step >= len(SCENARIOS[o.scenario]) for o in s.scalars(select(Order)).all())

    def run_to_end(self, max_ticks: int = 100) -> int:
        n = 0
        while not self.done() and n < max_ticks:
            self.tick()
            n += 1
        return n
