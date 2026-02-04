# Specification: Database Schema

## 1. Overview
This document defines the database schema for the Todo application. We use **Neon PostgreSQL** as the primary database and **SQLModel** (which combines SQLAlchemy and Pydantic) for ORM and type safety in the Python backend.

## 2. Tables

### 2.1. Users Table
Managed primarily by **Better Auth**. The backend stores a reference to these users.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | String | Primary Key | Unique identifier from Better Auth. |
| `email` | String | Unique, Not Null | User's email address. |
| `name` | String | Optional | User's display name. |
| `image` | String | Optional | URL to user's profile image. |

### 2.2. Tasks Table
Stores todo items associated with users.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto-inc | Unique task identifier. |
| `user_id` | String | Foreign Key (Users.id) | Owner of the task. |
| `title` | String | Not Null | Task summary. |
| `description`| Text | Optional | Detailed notes. |
| `status` | Enum | Default: 'PENDING' | 'PENDING' or 'COMPLETED'. |
| `created_at` | DateTime | Default: NOW() | Creation timestamp. |
| `updated_at` | DateTime | Default: NOW() | Last update timestamp. |

## 3. Performance & Indexes

To ensure fast lookups, the following indexes are required:
- `ix_tasks_user_id`: Index on `user_id` for efficient retrieval of a user's tasks.
- `ix_tasks_status`: Index on `status` to filter completed/pending tasks quickly.

## 4. SQLModel Definitions (Python)

```python
from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    image: Optional[str] = None
    
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="tasks")
```

## 5. Neon PostgreSQL Setup

### 5.1. Connection String
The application expects a `DATABASE_URL` environment variable:
`postgresql://[user]:[password]@[neon-hostname]/neondb?sslmode=require`

### 5.2. Initialization
- Use `SQLModel.metadata.create_all(engine)` for initial schema deployment.
- *Future*: Use **Alembic** for migrations when the schema evolves.

## 6. Acceptance Criteria

- **AC1**: Deleting a user should ideally handle associated tasks (cascade or restrict).
- **AC2**: Queries for `Tasks` filtered by `user_id` must use the index.
- **AC3**: The `updated_at` field must refresh on every update.
