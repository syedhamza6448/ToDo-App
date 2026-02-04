from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime

from todo_app.database import engine, get_session, init_db
from todo_app.models import Task, TaskCreate, TaskUpdate, TaskRead, TaskStatus, User
from todo_app.auth import get_current_user_id

app = FastAPI(title="Todo App API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/tasks", response_model=List[TaskRead])
def read_tasks(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    """List all tasks for the authenticated user."""
    statement = select(Task).where(Task.user_id == user_id).offset(offset).limit(limit)
    tasks = session.exec(statement).all()
    return tasks

@app.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """Create a new task for the authenticated user."""
    db_task = Task.model_validate(task_in, update={"user_id": user_id})
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """Get details of a specific task owned by the user."""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """Partially update a task's details."""
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = task_in.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}", response_model=TaskRead)
def replace_task(
    task_id: int,
    task_in: TaskCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """Replace task details (Update)."""
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.title = task_in.title
    db_task.description = task_in.description
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """Delete a task owned by the user."""
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(db_task)
    session.commit()
    return {"ok": True}

@app.patch("/tasks/{task_id}/toggle", response_model=TaskRead)
def toggle_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """Toggle task completion status."""
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.status = (
        TaskStatus.COMPLETED if db_task.status == TaskStatus.PENDING 
        else TaskStatus.PENDING
    )
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
