"""
routers/tasks.py

HTTP route handlers for the /tasks resource.
Implements full CRUD: Create (POST), Read (GET), Update (PATCH), Delete (DELETE).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repository import task_repository, project_repository

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task. Returns 404 if project_id does not match a real project."""
    project = project_repository.get_project_by_id(db, task_data.project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot create task: no project with id {task_data.project_id} exists.",
        )
    return task_repository.create_task(db, task_data)


@router.get("", response_model=list[schemas.TaskOut])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Return a paginated list of all tasks."""
    return task_repository.get_all_tasks(db, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Return a single task by ID. Returns 404 if it doesn't exist."""
    task = task_repository.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found.",
        )
    return task


@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Partially update a task (e.g. change its status).
    Returns 404 if no task exists with that ID."""
    task = task_repository.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found.",
        )
    return task_repository.update_task(db, task, task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task. Returns 404 if no task exists with that ID."""
    task = task_repository.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found.",
        )
    task_repository.delete_task(db, task)
    return None