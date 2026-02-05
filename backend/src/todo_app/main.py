from fastapi import FastAPI, HTTPException, Depends, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Any, Dict
from sqlmodel import Session, select, SQLModel
from datetime import datetime
from passlib.context import CryptContext # Import CryptContext for password hashing

# Placeholder for password hashing if passlib is not available.
# In a real application, use a strong hashing library like passlib or bcrypt.
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except ImportError:
    # Fallback if passlib is not installed
    print("Warning: passlib not found. Using a dummy password hash. Not secure for production.")
    class DummyCryptContext:
        def hash(self, password: str) -> str:
            return f"dummy_hashed_{password}"
        def verify(self, plain_password: str, hashed_password: str) -> bool:
            return hashed_password == f"dummy_hashed_{plain_password}"
    pwd_context = DummyCryptContext()


from todo_app.database import engine, get_session, init_db
from todo_app.models import Task, TaskCreate, TaskUpdate, TaskRead, TaskStatus, User
from todo_app.auth import get_current_user_id
from todo_app.agent import TodoAgent
from todo_app.chatkit import router as chatkit_router

app = FastAPI(title="Todo App API", version="1.0.0")

# Add CORS middleware
origins = [
    "http://localhost:3000",  # Frontend origin
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(chatkit_router, prefix="/api/chatkit", tags=["chatkit"])

class ChatRequest(SQLModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(SQLModel):
    conversation_id: int
    role: str
    content: str
    tools_used: List[str] = []

async def lifespan(app: FastAPI):
    init_db()
    yield

@app.post("/users", response_model=User, status_code=201) # Changed response model to User
async def create_user(
    user_in: Dict[str, str], # Expecting a dict with email, name, password
    session: Session = Depends(get_session)
):
    """Create a new user."""
    email = user_in.get("email")
    name = user_in.get("name")
    password = user_in.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Hash the password
    hashed_password = pwd_context.hash(password)

    # Create new user instance. Assuming 'id' can be the email or a UUID.
    # For simplicity, let's use email as ID for now if primary key is string.
    # If User.id is meant to be a UUID, a library like 'uuid' would be needed.
    # For now, using email as ID, which is not ideal for primary keys but common.
    # NOTE: If User.id MUST be a UUID, this part needs adjustment.
    new_user = User(
        id=email, # Using email as ID for simplicity, assuming it's unique and string
        email=email,
        name=name,
        password_hash=hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Chat with the AI agent.
    
    - **user_id**: Must match the authenticated user.
    - **message**: The user's input.
    - **conversation_id**: Optional ID to continue a conversation.
    """
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied: User ID mismatch")
    
    agent = TodoAgent(user_id=user_id)
    try:
        response = await agent.process_message(request.message, request.conversation_id)
        return ChatResponse(
            conversation_id=response["conversation_id"],
            role=response["role"],
            content=response["content"],
            tools_used=response.get("tools_used", [])
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Log error in production
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

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

