"""One module per runtime. Each exposes the same three coroutines:

    harness(ref, ask, mode) -> str                     answer one question / investigation
    looping(ref, io, mode) -> str                      run the always-on watcher until io says stop
    graph(ref, event, mode) -> (summary, path)         handle one carrier event with a fixed workflow
"""

import importlib

MODULES = {"langchain": "lc", "langgraph": "lg", "deepagents": "da", "adk": "adk", "adk_workflow": "adkwf", "claude": "claude"}


def get(runtime: str):  # noqa: ANN201
    return importlib.import_module(f"{__name__}.{MODULES[runtime]}")
