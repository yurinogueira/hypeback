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
	docker-compose run --rm server pytest

_flake8:
	docker-compose run --rm server flake8 --show-source .

_isort:
	docker-compose run --rm server isort --diff --check-only .

_isort-clear:
	docker-compose run --rm server isort .

lint: _flake8 _isort
format-code: _isort-clear
