from celery import Celery
from app.core.config import settings

# Initialize Celery app
celery_app = Celery(
    "migration_forecasting",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Celery beat schedule (periodic tasks)
celery_app.conf.beat_schedule = {
    "refresh-all-data": {
        "task": "app.workers.tasks.refresh_all_data",
        "schedule": 3600.0,  # Every hour (placeholder)
    },
    "recalculate-materialized-views": {
        "task": "app.workers.tasks.recalculate_materialized_views",
        "schedule": 7200.0,  # Every 2 hours (placeholder)
    },
}
