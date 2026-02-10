from app.celery_app import celery
from app.db_connections.mongo_connect import mongo
import logging

logger = logging.getLogger(__name__)

@celery.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3}, retry_backoff=True)
def store_event_task(self, event_dict):
  """
  Store validated GitHub event into MongoDB.
  Retries automatically on failure.
  """
  if mongo.events_collection is not None:
    mongo.database_connection()
  mongo.insert_event(event_dict)
  logger.info(f"Event stored via celery in Result DB-----------> {event_dict.get('action')} ")