from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

tasks = [
    {"id": 1, "title": "Task 1", "done": False},
    {"id": 2, "title": "Task 2", "done": False},
    {"id": 3, "title": "Task 3", "done": False},
]

@app.get("/")
async def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def read_health():
    return {"status": "healthy"}

@app.get("/tasks")
async def read_tasks():
    return tasks

@app.get("/tasks/{task_id}")
async def read_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

@app.post("/tasks")
async def create_task(task: dict):
    if task.get("title") == "" or task.get("title") is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Task title is required"}
        )
    new_task = {
        "id": max([task["id"] for task in tasks], default=0) + 1,
        "title": task.get("title"),
        "done": False
    }
    tasks.append(new_task)
    return JSONResponse(
        status_code=201,
        content= {"message": "Created"}
    )

@app.put("/tasks/{task_id}")
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

@app.delete("/tasks/{task_id}")
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

