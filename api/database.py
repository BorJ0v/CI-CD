import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use 'postgres' to match your docker-compose service name
DB_USER = os.getenv("POSTGRES_USER", "docask")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "docask_secret")
DB_NAME = os.getenv("POSTGRES_DB", "docask_db")

DATABASE_URL = "postgresql://docask:docask_secret@postgres:5432/docask""

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
