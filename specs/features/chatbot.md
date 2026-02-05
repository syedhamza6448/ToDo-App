# Specification: AI Chatbot & Agent

## 1. Overview
The AI Chatbot allows users to interact with their tasks using natural language. It leverages the **Model Context Protocol (MCP)** and **OpenAI Agents SDK** to interpret user intent and execute actions on the Todo database (e.g., "Remind me to buy milk").

## 2. Architecture
The architecture follows a stateless REST pattern where the backend manages the agent execution.

1.  **Frontend**: Chat interface sends user messages to the backend.
2.  **Backend (FastAPI)**:
    *   Receives the message.
    *   Retrieves conversation history from the database.
    *   Initializes an **OpenAI Agent** via the SDK.
    *   Connects the Agent to the internal **MCP Server**.
3.  **MCP Server**:
    *   Exposes project-specific tools (`get_tasks`, `add_task`, `complete_task`).
    *   Translates Agent tool calls into database queries using the `Task Manager`.
4.  **Database**: Persists conversations and messages for context continuity.

## 3. MCP Server Integration
We use the official **MCP SDK** to define the capabilities available to the LLM.

### 3.1. Tools
The following tools will be exposed via the MCP server:

| Tool Name | Arguments | Description |
| :--- | :--- | :--- |
| `create_task` | `title` (str), `description` (str, optional) | Creates a new task for the user. |
| `list_tasks` | `status` (str, optional), `limit` (int) | Lists the user's current tasks. |
| `update_task` | `task_id` (int), `status` (str, optional), `title` (str, optional) | Updates an existing task. |
| `delete_task` | `task_id` (int) | Deletes a task. |

### 3.2. Implementation Strategy
The MCP server runs within the same process as the FastAPI app (or as a localized module) to share the database connection pool.

## 4. OpenAI Agents SDK Integration
The system uses the **OpenAI Agents SDK** to orchestrate the reasoning loop.

- **Model**: `gpt-4o` (or equivalent capable model).
- **System Prompt**: Configured to act as a helpful productivity assistant. It must know today's date and the user's local context.
- **Tool Execution**: The SDK handles the tool calling loop (thinking -> tool call -> result -> response).

## 5. Database Models
New tables are required to store chat history.

### 5.1. Schema (SQLModel)

```python
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str = Field(description="user or assistant")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

## 6. Stateless Chat Endpoint Design

### 6.1. `POST /api/chat/messages`
Sends a new message to the agent.

- **Request Body**:
  ```json
  {
    "conversation_id": 123,  // Optional: creates new if null
    "content": "Add buy milk to my list"
  }
  ```
- **Process**:
  1. Authenticate user.
  2. Load previous messages for `conversation_id`.
  3. Invoke OpenAI Agent with history + new message.
  4. Agent queries MCP tools if needed.
  5. Save user message and agent response to DB.
- **Response**:
  ```json
  {
    "conversation_id": 123,
    "role": "assistant",
    "content": "I've added 'Buy milk' to your task list.",
    "tools_used": ["create_task"] // Optional debug info
  }
  ```

## 7. Natural Language Command Mapping

The Agent is responsible for parsing these intents:

| User Input | Intended Action | Tool Call |
| :--- | :--- | :--- |
| "I need to wash the car" | Create a task | `create_task(title="Wash the car")` |
| "What do I have to do?" | List pending tasks | `list_tasks(status="PENDING")` |
| "I finished the report" | Mark task as done | `list_tasks(search="report")` -> `update_task(id=..., status="COMPLETED")` |
| "Delete the old grocery task" | Remove a task | `list_tasks` -> `delete_task` |

## 8. Security
- **Data Isolation**: The MCP tools must strictly filter actions by the authenticated `user_id`. The agent must *never* access data belonging to other users.
- **Rate Limiting**: Apply strict limits on the chat endpoint to prevent API cost abuse.
