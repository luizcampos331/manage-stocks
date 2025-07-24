# Makefile

run:
	poetry run python app/run.py

reload:
	poetry run uvicorn app.main:app --reload

test:
	poetry run pytest

lint:
	poetry run ruff check .

fix:
	poetry run ruff check . --fix

format:
	poetry run ruff format .

install:
	poetry install

lock:
	poetry lock
