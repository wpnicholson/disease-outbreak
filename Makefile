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

## Create and apply migration in one step (not recommended for production)
quick-migrate:
	$(DC) exec $(SERVICE) bash -c "cd /code && alembic revision --autogenerate -m '$(message)' && alembic upgrade head"

## Wait for database to be ready before starting services
wait-db:
	$(DC) exec $(SERVICE) /wait-for-it.sh db:5432 --timeout=60 --strict -- echo "Database is up!"

## Reset and rebuild the entire environment, including migrations
reset-rebuild:
	$(DC) down --volumes --remove-orphans
	docker system prune -a --volumes -f
	$(DC) build
	$(DC) up -d
	$(DC) exec $(SERVICE) /wait-for-it.sh db:5432 --timeout=60 --strict -- echo "Database is ready!"
	$(DC) exec $(SERVICE) bash -c "cd /code && alembic revision --autogenerate -m '$(message)'"
	$(DC) exec $(SERVICE) bash -c "cd /code && alembic upgrade head"

## Lint with flake8
lint:
	$(DC) exec $(SERVICE) bash -c "cd /code && flake8 ."

## Format with black
format:
	$(DC) exec $(SERVICE) bash -c "cd /code && black ."

## Run FastAPI server manually (useful for debugging command override)
serve:
	$(DC) exec $(SERVICE) bash -c "cd /code && uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"

## Run tests (note: inside backend container)
test:
	$(DC) exec $(SERVICE) bash -c "cd /code && pytest tests"

## Run API tests with coverage report (note: inside backend container)
test-cov:
	$(DC) exec $(SERVICE) bash -c "cd /code && pytest --cov=api tests"

## Run API tests with verbose output (note: inside backend container)
test-verbose:
	$(DC) exec $(SERVICE) bash -c "cd /code && pytest -v tests"

## Seed database with sample data
seed:
	$(DC) exec $(SERVICE) bash -c "cd /code && python seed_data.py"
