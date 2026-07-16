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


