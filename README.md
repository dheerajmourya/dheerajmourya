# Task Management REST API

This is a RESTful Task Management System built with **Flask** and **PostgreSQL**. It supports users, projects, tasks, task dependencies, and includes token-based authentication (JWT).

## Features

- User Registration & Login (JWT Token)
- Create & Manage Projects
- Create Tasks under Projects
- Assign Tasks to Users
- Mark Task Status (`pending`, `in-progress`, `completed`)
- Add Dependencies to Tasks
- Prevent circular dependencies
- Prevent task completion until all dependencies are done
- Prevent user deletion if they have pending tasks

---

## Tech Stack

- **Flask** (no Flask-RESTful)
- **PostgreSQL** (with SQLAlchemy)
- **JWT** for authentication
- **Python 3.9+**

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd flask_task_api

## 2. Create & activate virtual environment
python -m venv venv
source venv/bin/activate

## 3. Install dependencies
pip install -r requirements.txt

## 4. Set up PostgreSQL database
CREATE DATABASE taskdb;


# Update your app/__init__.py file with your DB credentials:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/taskdb'


##5. Seed the database

python seed.py

## 6. Run the app
python run.py


###Authentication
##Register/Login (Get JWT token)

POST /auth/register
POST /auth/login

##Use JWT in all secured routes
Authorization: Bearer <your-token>


###API Endpoints Summary
##Users
    POST /auth/register – Register user

    POST /auth/login – Login and receive JWT token

    GET /users – List users (secured)

    GET /users/<id> – Get user by ID

    DELETE /users/<id> – Delete user (only if no pending/in-progress task)

##Projects
    POST /projects – Create project

    GET /projects – List all projects

    GET /projects/<id> – Get project by ID

    GET /projects/<id>/tasks – List all tasks in a project

##Tasks
    POST /projects/<project_id>/tasks – Create task (with optional dependencies)

    GET /tasks/<id> – Get task by ID

    PATCH /tasks/<id>/status – Update task status

    GET /users/<user_id>/tasks – Get tasks assigned to a user

    GET /tasks?status=pending – Filter tasks by status


###Logical Constraints
    task can't be marked as completed until all dependencies are completed.

    Circular task dependencies are not allowed.

    Users with pending/in-progress tasks cannot be deleted.


###Bonus
    JWT-based Authentication

    Pagination (optional)

    Unit test ready logic (can be added)


###Sample Users
alice@example.com

bob@example.com

Use /auth/login to get token for these.





