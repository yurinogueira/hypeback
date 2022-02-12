#!/bin/bash
.PHONY: default
.SILENT:


default:

build:
	docker-compose build --force-rm --no-cache --pull

bash:
	docker-compose run --rm server bash

shell:
	docker-compose run --rm server python manage.py shell

migrate:
	docker-compose run --rm server python manage.py migrate --noinput

migrations:
	docker-compose run --rm server python manage.py makemigrations $(app)

development:
	docker-compose run --rm --service-ports server python manage.py runserver 0:8000

createsuperuser:
	docker-compose run --rm server python manage.py createsuperuser

manage:
	docker-compose run --rm server python manage.py $(args)

# Queue
# -----------------------------------------------------------------------------
worker:
	@docker-compose run --rm server celery -A api worker -l INFO


beat:
	@docker-compose run --rm server celery -A api beat -l INFO

# Test and Code Quality
# -----------------------------------------------------------------------------
test:
	docker-compose run --rm --no-deps server pytest

_isort:
	docker-compose run --rm --no-deps server isort --diff --check-only .

_black:
	docker-compose run --rm --no-deps server black --check .

_mypy:
	docker-compose run --rm --no-deps server mypy . --exclude migrations

_isort-clear:
	docker-compose run --rm --no-deps server isort .

_black_fix:
	docker-compose run --rm --no-deps server black .

lint: _isort _black _mypy
format-code: _isort-clear _black_fix
