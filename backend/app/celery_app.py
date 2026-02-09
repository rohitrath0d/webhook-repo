from celery import Celery

celery = Celery(
    "webhook_worker",
    broker="redis://localhost:6379/0",
    backend="mongodb+srv://neelesh:pawar123@notes-taking-applicatio.3kj8jj2.mongodb.net/video-streaming-application?retryWrites=true&w=majority&appName=notes-taking-application"
)

celery.conf.update(
  task_serializer="json",
  accept_content=["json"],
  result_serializer="json"
)