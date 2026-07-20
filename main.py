from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import setup_db
import sqlite3

app = FastAPI()

setup_db()


@app.get("/")
async def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health", description="Check the health of the API")
async def read_health():
    return {"status": "healthy"}

@app.get("/tasks", description="Read all tasks")
async def read_tasks():
    con = sqlite3.connect("tasks.db")
    cur = con.cursor()
    tasks = cur.execute("select * from tasks").fetchall()
    return tasks

@app.get("/tasks/{task_id}", description="Read a task by ID")
async def read_task(task_id: int):
    con = sqlite3.connect("tasks.db")
    cur = con.cursor()
    task = cur.execute(f"select * from tasks WHERE id={task_id}").fetchone()
    if task:
        return task
    return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

@app.post("/tasks", description="Create a new task")
async def create_task(task: dict):
    if task.get("title") == "" or task.get("title") is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Task title is required"}
        )
    new_task = {
        "title": task.get("title"),
        "done": False
    }
    con = sqlite3.connect("tasks.db")
    cur = con.cursor()

    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.get("title"), False)
    )

    con.commit()
    con.close()

    return JSONResponse(
        status_code=201,
        content= {"message": "Created"}
    )

@app.put("/tasks/{task_id}", description="Update a task by ID")
async def update_task(task_id: int, task: dict):
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = task.get("title", t["title"])
            t["done"] = task.get("done", t["done"])
            return JSONResponse(
                status_code=200,
                content={"message": "Updated"}
            )
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

@app.delete("/tasks/{task_id}", description="Delete a task by ID")
async def delete_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return JSONResponse(
                status_code=200,
                content={"message": "Deleted"}
            )
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

