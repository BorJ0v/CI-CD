import os
from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = Celery("worker", broker=redis_url, backend=redis_url)

@app.task
def test_task(message: str):
    print(f"Worker received: {message}")
    return f"Processed: {message}"
