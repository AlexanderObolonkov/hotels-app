from celery import Celery

from app.config import settings

celery = Celery(
    "tasks",
    broker=settings.REDIS,
    include=["app.tasks.tasks"],
)
