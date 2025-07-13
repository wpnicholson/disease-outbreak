from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

if os.getenv("ENV") != "prod":
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        print(
            "Warning: dotenv module not found. Environment variables may not be loaded."
        )

DATABASE_URL: str | None = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    raise ValueError(f"Failed to create database engine: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
