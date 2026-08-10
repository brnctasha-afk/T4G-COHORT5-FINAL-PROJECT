"""
task_repository.py

Repository layer for Tasks.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas


def create_task(db: Session, task_data: schemas.TaskCreate) -> models.Task:
    """Insert a new task row into the database and return it."""
    new_task = models.Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        project_id=task_data.project_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_task_by_id(db: Session, task_id: int) -> Optional[models.Task]:
    """Fetch a single task by primary key, or None if it doesn't exist."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_all_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Task]:
    """Fetch a page of tasks, ordered by newest first."""
    return (
        db.query(models.Task)
        .order_by(models.Task.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_tasks_by_project(db: Session, project_id: int) -> List[models.Task]:
    """Fetch all tasks belonging to a specific project."""
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()


def update_task(
    db: Session, task: models.Task, task_data: schemas.TaskUpdate
) -> models.Task:
    """Apply only the fields the caller provided (partial update)."""
    update_fields = task_data.model_dump(exclude_unset=True)
    for field_name, value in update_fields.items():
        setattr(task, field_name, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: models.Task) -> None:
    """Delete a single task row."""
    db.delete(task)
    db.commit()