.PHONY: install run test all-usecases readmes up

install:
	pip install -r requirements.txt

run:
	uvicorn app.api:app --reload

test:
	python -m pytest -q

all-usecases:
	python scripts/run_all.py

readmes:
	python scripts/gen_readmes.py

up:
	docker compose up --build
