# Task Manager API

A full REST API built with **FastAPI**, **SQLAlchemy**, and **MySQL** for managing Users, Projects, and Tasks.

## What This Project Does

This API lets you:
- Create and manage **Users**
- Create **Projects** that belong to a User (one-to-many relationship)
- Create **Tasks** that belong to a Project (one-to-many relationship)
- Fetch a User's Projects, or a Project's Tasks, directly through the relationships
- Perform full CRUD (Create, Read, Update, Delete) on Projects and Tasks

**Relationship structure:**