#!/bin/bash

set -e

if [[ $COMMAND = "worker" ]]; then
    echo "Running Celery Worker"
    exec celery -A api worker -l INFO

elif [[ $COMMAND = "beat" ]]; then
    echo "Running Celery Beat"
    exec celery -A api beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

elif [[ $COMMAND = "development" ]]; then
    echo "Running development server"
    exec python -Wd manage.py runserver 0:8000

else
    echo "Running production server"
    exec gunicorn \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --threads 2 \
        --keep-alive 5 \
        --max-requests 1000 \
        --worker-connections=1000 \
        --access-logfile - \
        --error-logfile - \
        --log-level critical \
        --worker-class gevent \
        --reload \
        --capture-output \
        api.wsgi
fi
