"""
database.py

Handles the connection to our MySQL database using SQLAlchemy.

This file:
1. Reads database credentials from the .env file.
2. Encodes credentials to prevent syntax errors with special characters.
3. Builds a SQLAlchemy engine and SessionLocal factory.
4. Provides get_db() dependency for FastAPI routes.
"""

import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load variables from the .env file into the environment.
load_dotenv()

# Read database connection info from environment variables.
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# Fail fast if essential configuration is missing.
if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    raise RuntimeError(
        "Missing database configuration. "
        "Did you create a .env file based on .env.example?"
    )

# Encode password and user to handle special characters (@, #, :, /, etc.)
encoded_user = quote_plus(DB_USER)
encoded_password = quote_plus(DB_PASSWORD)

# Build the MySQL connection URL using PyMySQL driver.
DATABASE_URL = (
    f"mysql+pymysql://{encoded_user}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Engine manages the connection pool. pool_pre_ping prevents stale connection errors.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal is a factory that creates database sessions per request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for SQLAlchemy ORM models (models.py)
class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency to yield a database session and guarantee cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 