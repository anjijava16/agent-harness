.PHONY: install install-live demo test grok clean frameworks-lc frameworks-adk harness

install:
	pip install -r requirements.txt

install-live:
	pip install -r requirements-live.txt

demo:
	python run_all.py

test:
	PA_QUIET=1 python -m pytest -q

grok:
	python -m services.s01_grok_bot.grok_bot

clean:
	find . -name __pycache__ -type d -prune -exec rm -rf {} +

frameworks-lc:
	python -m venv .venv-lc && .venv-lc/bin/pip install -r requirements-langchain.txt && .venv-lc/bin/python frameworks/run_all.py

frameworks-adk:
	python -m venv .venv-adk && .venv-adk/bin/pip install -r requirements-adk.txt && .venv-adk/bin/python frameworks/run_all.py

harness:
	python harness_agents/examples/pi_style_minimal_harness.py
