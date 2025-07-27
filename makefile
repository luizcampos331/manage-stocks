run:
	poetry run python app/run.py

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=app --cov-report=term --cov-report=html

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

# Alembic commands
migrate:
	poetry run alembic upgrade head

migrate-create:
	poetry run alembic revision -m "$(message)"

migrate-current:
	poetry run alembic current

migrate-history:
	poetry run alembic history

migrate-downgrade:
	poetry run alembic downgrade -1

migrate-downgrade-base:
	poetry run alembic downgrade base

migrate-stamp:
	poetry run alembic stamp head

migrate-show:
	poetry run alembic show
