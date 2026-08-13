# Task Manager REST API

## Project Description

The Task Manager REST API is a backend application built using FastAPI, SQLAlchemy, and MySQL. It allows users to create and manage projects and tasks. Each user can have multiple projects, and each project can contain multiple tasks.

This project was developed as the final project for the Tech4Girls Cohort 5 Backend Development Program.

---

## Features

- Create, view, update, and delete users
- Create, view, update, and delete projects
- Create, view, update, and delete tasks
- MySQL database integration
- SQLAlchemy ORM
- Repository pattern
- Environment variables using `.env`
- Proper HTTP status codes
- Error handling

---

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Uvicorn
- python-dotenv

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/brnctasha-afk/t4g-cohort5-final-project.git
```

2. Open the project folder:

```bash
cd t4g-cohort5-final-project
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

5. Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project folder and add your database credentials:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=task_manager
DB_USER=root
DB_PASSWORD=your_password
```

---

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Then open your browser and visit:

```
http://127.0.0.1:8000/docs
```

This opens the Swagger UI where you can test all the API endpoints.

---

## API Endpoints

### Users

- POST `/users`
- GET `/users`
- GET `/users/{id}`
- PUT `/users/{id}`
- DELETE `/users/{id}`

### Projects

- POST `/projects`
- GET `/projects`
- GET `/projects/{id}`
- PUT `/projects/{id}`
- DELETE `/projects/{id}`

### Tasks

- POST `/tasks`
- GET `/tasks`
- GET `/tasks/{id}`
- PATCH `/tasks/{id}`
- DELETE `/tasks/{id}`

---

## Database Relationship

- One User can have many Projects.
- One Project can have many Tasks.

---

## HTTP Status Codes

- **200 OK** – Request successful
- **201 Created** – Resource created
- **204 No Content** – Resource deleted
- **400 Bad Request** – Invalid request
- **404 Not Found** – Resource not found
- **422 Unprocessable Entity** – Validation error
- **500 Internal Server Error** – Server error

---

## Author

**Tekpor Bernice Yawa**

Tech4Girls Cohort 5 – Backend Development Final Project