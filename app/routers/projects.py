"""
routers/projects.py

HTTP route handlers for the /projects resource.
Implements full CRUD: Create (POST), Read (GET), Update (PUT), Delete (DELETE).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repository import project_repository, user_repository, task_repository

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(project_data: schemas.ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project. Returns 404 if the owner_id does not match a real user."""
    owner = user_repository.get_user_by_id(db, project_data.owner_id)
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot create project: no user with id {project_data.owner_id} exists.",
        )
    return project_repository.create_project(db, project_data)


@router.get("", response_model=list[schemas.ProjectOut])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Return a paginated list of all projects."""
    return project_repository.get_all_projects(db, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=schemas.ProjectWithTasksOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Return a single project along with its tasks.
    Returns 404 if no project exists with that ID."""
    project = project_repository.get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} was not found.",
        )
    return project


@router.get("/{project_id}/tasks", response_model=list[schemas.TaskOut])
def get_tasks_for_project(project_id: int, db: Session = Depends(get_db)):
    """Return all tasks that belong to a specific project."""
    project = project_repository.get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} was not found.",
        )
    return task_repository.get_tasks_by_project(db, project_id)


@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(
    project_id: int, project_data: schemas.ProjectUpdate, db: Session = Depends(get_db)
):
    """Update an existing project's name and/or description.
    Returns 404 if no project exists with that ID."""
    project = project_repository.get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} was not found.",
        )
    return project_repository.update_project(db, project, project_data)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project (and cascade-delete its tasks).
    Returns 404 if no project exists with that ID."""
    project = project_repository.get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} was not found.",
        )
    project_repository.delete_project(db, project)
    return None