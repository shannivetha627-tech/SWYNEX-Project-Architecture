# SWYNEX Project Architecture — TaskFlow Lite

A small task-management web application built with FastAPI, SQLite, and HTML/CSS/JavaScript.

## Features
- Create a task with a title and optional description
- View all tasks
- Mark a task as completed or pending
- Edit task details
- Delete a task

## Tech stack
- Backend: Python 3.11+, FastAPI
- Database: SQLite
- Frontend: HTML, CSS, vanilla JavaScript
- API documentation: FastAPI Swagger UI (`/docs`)

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

## Project structure
```text
SWYNEX-Project-Architecture/
├── app/
│   ├── static/style.css
│   ├── templates/index.html
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## Initial scope
This starter is intentionally limited to a single-user task list. Authentication, teams, notifications,
file attachments, and third-party integrations are out of scope for version 1.

## Intended repository URL
https://github.com/shannivetha627-tech/SWYNEX-Project-Architecture

This is the proposed URL only. Create the public GitHub repository with this exact name and push these files
before sharing the link.
