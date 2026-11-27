# frameworks/

28 runnable examples against the real libraries, offline by default.

| Folder | Library (checked) | Examples | Deep dive |
|---|---|---|---|
| `langchain/` | langchain 1.5.2 | 5 | [README](langchain/README.md) |
| `langgraph/` | langgraph 1.2.24 | 6 | [README](langgraph/README.md) |
| `deep_agents/` | deepagents 0.7.42 | 5 | [README](deep_agents/README.md) |
| `google_adk/` | google-adk 2.15.1 | 5 | [README](google_adk/README.md) |
| `google_adk_workflows/` | google-adk 2.15.1 | 7 | [README](google_adk_workflows/README.md) |

How offline works: `_fakes/lc_fake.py` is a `GenericFakeChatModel` that accepts `bind_tools`; `_fakes/adk_fake.py` is a `BaseLlm` subclass. Both replay scripted model turns. Everything else is the real framework. Pass `--live` to use a real model (`LC_MODEL=...` or `GOOGLE_API_KEY`).

```bash
python -m venv .venv-lc  && .venv-lc/bin/pip install -r ../requirements-langchain.txt && .venv-lc/bin/python run_all.py
python -m venv .venv-adk && .venv-adk/bin/pip install -r ../requirements-adk.txt     && .venv-adk/bin/python run_all.py
```

The overview is in [../UpdatedREADME.md](../UpdatedREADME.md).
