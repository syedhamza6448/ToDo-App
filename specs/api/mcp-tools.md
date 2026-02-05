# Specification: MCP Tools

## 1. Overview
This document defines the Model Context Protocol (MCP) tools exposed by the Todo application. These tools allow AI agents and external clients to interact with the task management system programmatically.

All tools operate within the context of the authenticated user. Operations are strictly scoped to the user's data.

## 2. Tools Definitions

### 2.1. add_task
Creates a new task with a title and an optional description.

*   **Name**: `add_task`
*   **Description**: Create a new task in the user's todo list.
*   **Parameters (JSON Schema)**:
    ```json
    {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "The title of the task. Must not be empty."
        },
        "description": {
          "type": "string",
          "description": "Detailed description of the task."
        }
      },
      "required": ["title"]
    }
    ```
*   **Returns**: The created task object including its generated ID and timestamps.
*   **Example Input**:
    ```json
    {
      "title": "Buy groceries",
      "description": "Milk, Bread, Eggs"
    }
    ```
*   **Example Output**:
    ```json
    {
      "id": 101,
      "title": "Buy groceries",
      "description": "Milk, Bread, Eggs",
      "status": "PENDING",
      "created_at": "2023-10-27T10:00:00Z",
      "updated_at": "2023-10-27T10:00:00Z"
    }
    ```

### 2.2. list_tasks
Retrieves a list of tasks, optionally filtered by their status.

*   **Name**: `list_tasks`
*   **Description**: Get all tasks or filter by status (PENDING/COMPLETED).
*   **Parameters (JSON Schema)**:
    ```json
    {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": ["PENDING", "COMPLETED"],
          "description": "Filter tasks by status. If omitted, returns all tasks."
        }
      }
    }
    ```
*   **Returns**: An array of task objects.
*   **Example Input**:
    ```json
    {
      "status": "PENDING"
    }
    ```
*   **Example Output**:
    ```json
    [
      {
        "id": 101,
        "title": "Buy groceries",
        "description": "Milk, Bread, Eggs",
        "status": "PENDING",
        "created_at": "2023-10-27T10:00:00Z",
        "updated_at": "2023-10-27T10:00:00Z"
      }
    ]
    ```

### 2.3. complete_task
Mark a task as completed (or toggle its status).

*   **Name**: `complete_task`
*   **Description**: Mark a specific task as COMPLETED. If the task is already completed, this operation makes it PENDING (toggles).
*   **Parameters (JSON Schema)**:
    ```json
    {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "The unique ID of the task to complete."
        }
      },
      "required": ["task_id"]
    }
    ```
*   **Returns**: The updated task object showing the new status.
*   **Example Input**:
    ```json
    {
      "task_id": 101
    }
    ```
*   **Example Output**:
    ```json
    {
      "id": 101,
      "title": "Buy groceries",
      "description": "Milk, Bread, Eggs",
      "status": "COMPLETED",
      "created_at": "2023-10-27T10:00:00Z",
      "updated_at": "2023-10-27T12:00:00Z"
    }
    ```

### 2.4. delete_task
Permanently removes a task.

*   **Name**: `delete_task`
*   **Description**: Delete a task by its ID.
*   **Parameters (JSON Schema)**:
    ```json
    {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "The unique ID of the task to delete."
        }
      },
      "required": ["task_id"]
    }
    ```
*   **Returns**: A confirmation message or boolean indicating success.
*   **Example Input**:
    ```json
    {
      "task_id": 101
    }
    ```
*   **Example Output**:
    ```json
    {
      "success": true,
      "message": "Task 101 deleted successfully."
    }
    ```

### 2.5. update_task
Modifies the title or description of an existing task.

*   **Name**: `update_task`
*   **Description**: Update the details of a task.
*   **Parameters (JSON Schema)**:
    ```json
    {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "The unique ID of the task to update."
        },
        "title": {
          "type": "string",
          "description": "New title for the task."
        },
        "description": {
          "type": "string",
          "description": "New description for the task."
        }
      },
      "required": ["task_id"]
    }
    ```
*   **Returns**: The updated task object.
*   **Example Input**:
    ```json
    {
      "task_id": 101,
      "title": "Buy organic groceries"
    }
    ```
*   **Example Output**:
    ```json
    {
      "id": 101,
      "title": "Buy organic groceries",
      "description": "Milk, Bread, Eggs",
      "status": "PENDING",
      "created_at": "2023-10-27T10:00:00Z",
      "updated_at": "2023-10-27T10:05:00Z"
    }
    ```

## 3. Error Handling

All tools adhere to a standard error format.

### 3.1. Common Errors

| Error Code | Meaning | Description |
| :--- | :--- | :--- |
| `VALIDATION_ERROR` | Invalid Input | The parameters provided do not match the schema (e.g., missing required field, wrong type). |
| `NOT_FOUND` | Resource Not Found | The specified `task_id` does not exist or does not belong to the authenticated user. |
| `UNAUTHORIZED` | Auth Failure | The user is not authenticated. |
| `INTERNAL_ERROR` | Server Error | An unexpected error occurred on the server. |

### 3.2. Error Response Structure

```json
{
  "error": true,
  "code": "NOT_FOUND",
  "message": "Task with ID 101 not found."
}
```
