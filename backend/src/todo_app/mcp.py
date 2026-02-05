import os
import json
from datetime import datetime
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select
from todo_app.database import engine, init_db
from todo_app.models import Task, TaskStatus, User

# Initialize FastMCP server
mcp = FastMCP("Todo App")

# Helper to get session
def get_session():
    return Session(engine)

# Helper to get or create the MCP user
def get_mcp_user_id(session: Session) -> str:
    user_id = os.getenv("MCP_USER_ID", "mcp-user")
    user = session.get(User, user_id)
    if not user:
        # Create the user if it doesn't exist to avoid FK errors
        user = User(id=user_id, email=f"{user_id}@example.com", name="MCP User")
        session.add(user)
        session.commit()
    return user_id

@mcp.tool()
def add_task(title: str, description: str = "") -> str:
    """
    Create a new task in the user's todo list.
    
    Args:
        title: The title of the task. Must not be empty.
        description: Detailed description of the task.
    """
    if not title:
        return json.dumps({"error": True, "code": "VALIDATION_ERROR", "message": "Title is required."})

    with get_session() as session:
        user_id = get_mcp_user_id(session)
        task = Task(title=title, description=description, user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task.model_dump_json()

@mcp.tool()
def list_tasks(status: Optional[str] = None) -> str:
    """
    Get all tasks or filter by status (PENDING/COMPLETED).
    
    Args:
        status: Filter tasks by status. If omitted, returns all tasks.
    """
    with get_session() as session:
        user_id = get_mcp_user_id(session)
        query = select(Task).where(Task.user_id == user_id)
        
        if status:
            try:
                task_status = TaskStatus(status.upper())
                query = query.where(Task.status == task_status)
            except ValueError:
                return json.dumps({
                    "error": True, 
                    "code": "VALIDATION_ERROR", 
                    "message": f"Invalid status '{status}'. Must be PENDING or COMPLETED."
                })
        
        tasks = session.exec(query).all()
        # Return JSON string array
        return json.dumps([task.model_dump() for task in tasks], default=str)

@mcp.tool()
def complete_task(task_id: int) -> str:
    """
    Mark a specific task as COMPLETED. If the task is already completed, this operation makes it PENDING (toggles).
    
    Args:
        task_id: The unique ID of the task to complete.
    """
    with get_session() as session:
        user_id = get_mcp_user_id(session)
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return json.dumps({
                "error": True, 
                "code": "NOT_FOUND", 
                "message": f"Task with ID {task_id} not found."
            })
        
        if task.status == TaskStatus.PENDING:
            task.status = TaskStatus.COMPLETED
        else:
            task.status = TaskStatus.PENDING
        
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task.model_dump_json()

@mcp.tool()
def delete_task(task_id: int) -> str:
    """
    Delete a task by its ID.
    
    Args:
        task_id: The unique ID of the task to delete.
    """
    with get_session() as session:
        user_id = get_mcp_user_id(session)
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
             return json.dumps({
                "error": True, 
                "code": "NOT_FOUND", 
                "message": f"Task with ID {task_id} not found."
            })
        
        session.delete(task)
        session.commit()
        return json.dumps({
            "success": True, 
            "message": f"Task {task_id} deleted successfully."
        })

@mcp.tool()
def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> str:
    """
    Update the details of a task.
    
    Args:
        task_id: The unique ID of the task to update.
        title: New title for the task.
        description: New description for the task.
    """
    with get_session() as session:
        user_id = get_mcp_user_id(session)
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return json.dumps({
                "error": True, 
                "code": "NOT_FOUND", 
                "message": f"Task with ID {task_id} not found."
            })
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
            
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task.model_dump_json()

if __name__ == "__main__":
    # Ensure DB is initialized
    init_db()
    # Run the MCP server
    mcp.run()
