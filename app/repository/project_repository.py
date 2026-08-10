"""
project_repository.py

Repository layer for Projects.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas


def create_project(db: Session, project_data: schemas.ProjectCreate) -> models.Project:
    """Insert a new project row into the database and return it."""
    new_project = models.Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=project_data.owner_id,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def get_project_by_id(db: Session, project_id: int) -> Optional[models.Project]:
    """Fetch a single project by primary key, or None if it doesn't exist."""
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_all_projects(db: Session, skip: int = 0, limit: int = 100) -> List[models.Project]:
    """Fetch a page of projects, ordered by newest first."""
    return (
        db.query(models.Project)
        .order_by(models.Project.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_projects_by_owner(db: Session, owner_id: int) -> List[models.Project]:
    """Fetch all projects that belong to a specific user."""
    return db.query(models.Project).filter(models.Project.owner_id == owner_id).all()


def update_project(
    db: Session, project: models.Project, project_data: schemas.ProjectUpdate
) -> models.Project:
    """Apply only the fields the caller provided (partial update)."""
    update_fields = project_data.model_dump(exclude_unset=True)
    for field_name, value in update_fields.items():
        setattr(project, field_name, value)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: models.Project) -> None:
    """Delete a project row. Its tasks cascade-delete automatically."""
    db.delete(project)
    db.commit()