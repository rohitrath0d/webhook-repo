from celery import Celery
import os

celery = Celery(
    "webhook_worker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("DATABASE_URL"),
)

celery.conf.update(
    mongodb_backend_settings={
      "taskmeta_collection": "celery_task_metadata"
    },
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
