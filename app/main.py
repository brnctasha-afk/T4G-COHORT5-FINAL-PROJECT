"""
main.py

The entrypoint for our FastAPI application.

To run this app:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.database import Base, engine
from app.routers import users, projects, tasks

# Create all tables defined in models.py if they don't already exist.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description=(
        "A REST API for managing Users, Projects, and Tasks. "
        "Users own Projects, and Projects contain Tasks."
    ),
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/", tags=["Health"])
def read_root():
    """Simple health-check endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Task Manager API is running."}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Triggered when incoming request data fails Pydantic validation."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation failed", "details": exc.errors()},
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Triggered on any unexpected database error."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "A database error occurred. Please try again later."},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all safety net for any error type we didn't anticipate."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "An unexpected error occurred. Please try again later."},
    )