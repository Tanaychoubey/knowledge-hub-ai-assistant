from celery import Celery
from app.core.config import settings

celery = Celery(
    "knowledge_hub_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.worker.tasks"]
)

# Standard Celery settings optimized for local tasks
celery.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Solve concurrency lockups inside standard Docker setups
    worker_prefetch_multiplier=1,
)
