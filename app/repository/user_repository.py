"""
user_repository.py

The "repository layer" for Users. All direct SQLAlchemy queries for the
User model live here, separate from route handlers.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas


def create_user(db: Session, user_data: schemas.UserCreate) -> models.User:
    """Insert a new user row into the database and return it."""
    new_user = models.User(name=user_data.name, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """Fetch a single user by primary key, or None if it doesn't exist."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Fetch a single user by email — used to check for duplicates."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Fetch a page of users, ordered by newest first."""
    return (
        db.query(models.User)
        .order_by(models.User.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_user(db: Session, user: models.User) -> None:
    """Delete a user row. Their projects/tasks cascade-delete automatically."""
    db.delete(user)
    db.commit()