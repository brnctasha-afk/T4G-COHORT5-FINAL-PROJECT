# Task Manager API

A REST API built with FastAPI, SQLAlchemy, and MySQL for managing Users, Projects, and Tasks.

## What it does

- Users own Projects (one-to-many)
- Projects contain Tasks (one-to-many)
- Full CRUD on Projects and Tasks
- Deleting a User or Project cascades and deletes their related records

## Setup

1. Clone the repo and enter the folder
2. Create a virtual environment: `python3 -m venv venv` then `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Create the MySQL database: `CREATE DATABASE task_manager_db;`
5. Copy `.env.example` to `.env` and fill in your real MySQL credentials
6. Run the API: `uvicorn app.main:app --reload`
7. Open the docs: http://127.0.0.1:8000/docs

## Endpoints

- Users: POST/GET `/users`, GET/DELETE `/users/{id}`
- Projects: POST/GET `/projects`, GET/PUT/DELETE `/projects/{id}`, GET `/projects/{id}/tasks`
- Tasks: POST/GET `/tasks`, GET/PATCH/DELETE `/tasks/{id}`

## Tech Stack

FastAPI, SQLAlchemy, MySQL, Pydantic, python-dotenv, Uvicorn