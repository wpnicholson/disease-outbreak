# Makefile for Disease Outbreak Reporting System (Dev Workflow)

DC=docker-compose -f docker-compose.dev.yml
SERVICE=backend-app

## Build all images
build:
	$(DC) build

## Stop and remove all containers, volumes, and orphans
reset:
	$(DC) down --volumes --remove-orphans
	docker system prune -a --volumes -f

## Start all services in the background
up:
	$(DC) up -d

## Stop all services
down:
	$(DC) down

## Attach to logs
logs:
	$(DC) logs -f $(SERVICE)

## Bash into backend container
bash:
	$(DC) exec $(SERVICE) bash

## Create new Alembic revision (usage: make migrate message="your message")
migrate:
	$(DC) exec $(SERVICE) bash -c "cd /code && alembic revision --autogenerate -m '$(message)'"

## Apply all Alembic migrations
upgrade:
	$(DC) exec $(SERVICE) bash -c "cd /code && alembic upgrade head"

## Run tests (inside backend container)
test:
	$(DC) exec $(SERVICE) bash -c "cd /code && pytest backend/tests"

## Lint with flake8
lint:
	$(DC) exec $(SERVICE) bash -c "cd /code && flake8 ."

## Format with black
format:
	$(DC) exec $(SERVICE) bash -c "cd /code && black ."

## Run FastAPI server manually (useful for debugging command override)
serve:
	$(DC) exec $(SERVICE) bash -c "cd /code && uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"

## Run tests from project root (basic)
pytest-root:
	pytest backend/tests

## Run tests with coverage report
pytest-cov:
	pytest --cov=backend/api backend/tests

## Run tests with verbose output
pytest-verbose:
	pytest -v backend/tests
