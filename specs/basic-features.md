# Specification: Basic Todo Features

## 1. Overview
This specification defines the core functionality for a Console Interface (CLI) Todo application. The application allows users to manage a list of tasks with basic CRUD (Create, Read, Update, Delete) operations and completion status tracking.

## 2. Data Structures

### 2.1. Task Model
A single unit of work to be tracked.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Unique identifier for the task (auto-incrementing starting at 1). |
| `title` | String | Short summary of the task (required). |
| `description` | String | Detailed information about the task (optional). |
| `status` | Enum | Current state: `PENDING` (default) or `COMPLETED`. |
| `created_at` | DateTime | Timestamp when the task was created. |
| `updated_at` | DateTime | Timestamp when the task was last modified. |

### 2.2. Storage
- Tasks will be stored in memory for the initial prototype.
- *Future Consideration*: JSON file persistence.

## 3. User Interaction Flow

The application presents a main menu loop:

```text
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Completion
6. Exit
Select an option: 
```

### 3.1. Add Task
1. User selects "Add Task".
2. System prompts for `Title`.
3. System prompts for `Description` (can be empty).
4. System creates task with `status=PENDING`.
5. System confirms creation: "Task [ID] created successfully."

### 3.2. View Tasks
1. User selects "View Tasks".
2. System displays table/list of tasks.
3. Format: `[ID] [Status] Title - Description`
   - Example: `[1] [ ] Buy Milk - 2% fat`
   - Example: `[2] [X] Walk Dog - In the park`

### 3.3. Update Task
1. User selects "Update Task".
2. System asks for `Task ID`.
3. If ID not found, show error.
4. System prompts for new `Title` (leave blank to keep current).
5. System prompts for new `Description` (leave blank to keep current).
6. System updates task and `updated_at` timestamp.
7. System confirms update.

### 3.4. Delete Task
1. User selects "Delete Task".
2. System asks for `Task ID`.
3. If ID not found, show error.
4. System deletes the task.
5. System confirms deletion.

### 3.5. Toggle Completion
1. User selects "Toggle Completion".
2. System asks for `Task ID`.
3. If ID not found, show error.
4. If status is `PENDING`, change to `COMPLETED`.
5. If status is `COMPLETED`, change to `PENDING`.
6. System confirms new status.

## 4. Acceptance Criteria

### AC1: Task Creation
- **Given** the user is on the Add Task screen
- **When** they enter a valid title "Groceries" and description "Buy apples"
- **Then** a new task is stored with a unique ID and "PENDING" status.

### AC2: Listing Tasks
- **Given** there are existing tasks
- **When** the user views the list
- **Then** all tasks are displayed with their ID, correct status indicator ([ ] or [X]), title, and description.

### AC3: Deleting Tasks
- **Given** a task with ID 1 exists
- **When** the user deletes task ID 1
- **Then** the task is removed from the list and cannot be retrieved.

### AC4: Updating Tasks
- **Given** a task exists
- **When** the user updates the title
- **Then** the task reflects the new title, but the ID and status remain unchanged.

### AC5: Completion Toggling
- **Given** a pending task
- **When** the user toggles completion
- **Then** the task status becomes `COMPLETED`.
- **And** repeating the action makes it `PENDING` again.
