import os
from celery import Celery
from .database import SessionLocal

# Matches the 'redis' service in your YAML
CELERY_BROKER = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("tasks", broker=CELERY_BROKER)

@celery_app.task(name="process_pdf_task")
def process_pdf_task(doc_id, file_bytes):
    # Logic for OpenAI goes here later
    pass
