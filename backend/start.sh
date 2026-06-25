#!/bin/bash

# Start Celery worker in the background
echo "Starting Celery background worker..."
celery -A app.worker.celery_app.celery worker --loglevel=info --pool=solo &

# Start FastAPI Web Server in the foreground
echo "Starting Uvicorn API server on port 8000..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
