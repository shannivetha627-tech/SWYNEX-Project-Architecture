from pathlib import Path
import sqlite3
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import get_connection, initialize_database
from .schemas import TaskCreate, TaskUpdate

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="TaskFlow Lite API", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.on_event("startup")
def startup():
    initialize_database()

def row_to_dict(row):
    item = dict(row)
    item["is_completed"] = bool(item["is_completed"])
    return item

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/tasks")
def list_tasks():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC, id DESC"
        ).fetchall()
    return [row_to_dict(row) for row in rows]

@app.post("/api/tasks", status_code=201)
def create_task(payload: TaskCreate):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Title cannot be blank")
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (title, payload.description.strip())
        )
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return row_to_dict(row)

@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Title cannot be blank")
    with get_connection() as connection:
        cursor = connection.execute(
            """UPDATE tasks
               SET title = ?, description = ?, is_completed = ?,
                   updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (title, payload.description.strip(), int(payload.is_completed), task_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
    return row_to_dict(row)

@app.patch("/api/tasks/{task_id}/status")
def toggle_task_status(task_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")
        new_status = 0 if row["is_completed"] else 1
        connection.execute(
            "UPDATE tasks SET is_completed = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (new_status, task_id)
        )
        updated = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
    return row_to_dict(updated)

@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
    return None
