from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from api.models import Base  # noqa: F401

# Always load .env file first
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    if os.getenv("ENV") != "prod":
        print("Warning: dotenv not installed. Environment variables may not be loaded.")


# Get DATABASE_URL
DATABASE_URL: str | None = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Create sync engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Create session factory (sync)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
