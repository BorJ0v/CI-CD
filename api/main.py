import os
from fastapi import FastAPI
import psycopg2
import redis

app = FastAPI(title="DocAsk API")

@app.get("/health")
def health():
    return {"status": "ok", "service": "api"}

@app.get("/health/postgres")
def health_postgres():
    try:
        conn = psycopg2.connect(
            host="postgres",
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        conn.close()
        return {"status": "ok", "service": "postgres"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/health/redis")
def health_redis():
    try:
        r = redis.from_url(os.getenv("REDIS_URL"))
        r.ping()
        return {"status": "ok", "service": "redis"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
