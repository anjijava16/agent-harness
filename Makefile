.PHONY: install install-live demo test grok clean

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
