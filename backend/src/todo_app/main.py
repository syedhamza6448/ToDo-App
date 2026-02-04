from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from todo_app.manager import TodoManager
from todo_app.models import TaskStatus

app = FastAPI(title="Todo App API")
manager = TodoManager()

# Pydantic models for API requests/responses
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    
    class Config:
        from_attributes = True

@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks():
    tasks = manager.get_all_tasks()
    return [{"id": t.id, "title": t.title, "description": t.description, "status": t.status.value} for t in tasks]

@app.post("/tasks", response_model=TaskResponse)
async def create_task(task_in: TaskCreate):
    task = manager.add_task(task_in.title, task_in.description)
    return {"id": task.id, "title": task.title, "description": task.description, "status": task.status.value}

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    task = manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task.id, "title": task.title, "description": task.description, "status": task.status.value}

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_in: TaskUpdate):
    task = manager.update_task(task_id, title=task_in.title, description=task_in.description)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task.id, "title": task.title, "description": task.description, "status": task.status.value}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    if not manager.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

@app.post("/tasks/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task(task_id: int):
    task = manager.toggle_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task.id, "title": task.title, "description": task.description, "status": task.status.value}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)