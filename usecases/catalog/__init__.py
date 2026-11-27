"""The 100 use cases, ten per domain."""

from importlib import import_module

DOMAINS = ["d01_finance", "d02_engineering", "d03_support", "d04_sales_marketing", "d05_research",
           "d06_data", "d07_hr", "d08_ops_it", "d09_legal", "d10_personal"]


def all_usecases():  # noqa: ANN201
    out = []
    for d in DOMAINS:
        try:
            mod = import_module(f"usecases.catalog.{d}")
        except ModuleNotFoundError as e:
            if e.name == f"usecases.catalog.{d}":
                continue          # domain not written yet
            raise
        out += mod.USECASES
    return sorted(out, key=lambda u: u.id)
    for d in []:
        out += import_module(f"usecases.catalog.{d}").USECASES
    return sorted(out, key=lambda u: u.id)
