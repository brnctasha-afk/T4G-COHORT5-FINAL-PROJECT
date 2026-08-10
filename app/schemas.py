"""
schemas.py

Pydantic models used to:
1. Validate incoming request data.
2. Shape outgoing response data.

Naming convention:
- "...Create"  -> data required to create a new record
- "...Update"  -> data allowed when updating an existing record (all optional)
- "...Out"     -> data returned to the client in a response
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from app.models import TaskStatus


# ---------------------------------------------------------------------------
# User schemas
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Jane Doe"])
    email: EmailStr = Field(..., examples=["jane@example.com"])


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserWithProjectsOut(UserOut):
    """User response that also nests their projects."""
    projects: List["ProjectOut"] = []


# ---------------------------------------------------------------------------
# Project schemas
# ---------------------------------------------------------------------------

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150, examples=["Website Redesign"])
    description: Optional[str] = Field(None, examples=["Redesign the marketing site"])
    owner_id: int = Field(..., gt=0, description="ID of the user who owns this project")


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectWithTasksOut(ProjectOut):
    """Project response that also nests its tasks."""
    tasks: List["TaskOut"] = []


# ---------------------------------------------------------------------------
# Task schemas
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, examples=["Design homepage mockup"])
    description: Optional[str] = Field(None, examples=["Create a Figma mockup for the new homepage"])
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    project_id: int = Field(..., gt=0, description="ID of the project this task belongs to")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Resolve the forward references used above.
UserWithProjectsOut.model_rebuild()
ProjectWithTasksOut.model_rebuild()