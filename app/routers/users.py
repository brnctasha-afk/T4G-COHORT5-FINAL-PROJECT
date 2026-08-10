"""
routers/users.py

HTTP route handlers for the /users resource.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repository import user_repository

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user. Returns 409 if the email is already registered."""
    existing_user = user_repository.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with email '{user_data.email}' already exists.",
        )
    return user_repository.create_user(db, user_data)


@router.get("", response_model=list[schemas.UserOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Return a paginated list of all users."""
    return user_repository.get_all_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.UserWithProjectsOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Return a single user along with the projects they own.
    Returns 404 if no user exists with that ID."""
    user = user_repository.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} was not found.",
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user (and cascade-delete their projects/tasks).
    Returns 404 if no user exists with that ID."""
    user = user_repository.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} was not found.",
        )
    user_repository.delete_user(db, user)
    return None