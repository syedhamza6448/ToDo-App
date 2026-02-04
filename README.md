# Python Todo App

A Python-based Todo application built with `uv`.

## Project Structure

- `src/`: Source code.
- `specs/`: Specifications for features.
- `Constitution.md`: Development principles.

## Prerequisites

- Python 3.13+
- `uv` (Universal Python Package Manager)

## Setup

1.  **Install `uv`** (if not installed):
    ```bash
    pip install uv
    # or follow official instructions at https://github.com/astral-sh/uv
    ```

2.  **Initialize/Sync Dependencies**:
    ```bash
    uv sync
    ```

## Usage

Run the application:

```bash
uv run src/todo_app/main.py
```

### Examples

**Adding a Task:**
```text
Select an option: 1
--- Add Task ---
Title: Buy Groceries
Description: Milk, Eggs, Bread
Task [1] created successfully.
```

**Viewing Tasks:**
```text
Select an option: 2
--- Task List ---
[1] [ ] Buy Groceries - Milk, Eggs, Bread
```

**Completing a Task:**
```text
Select an option: 5
--- Toggle Completion ---
Task ID: 1
Task 1 status changed to COMPLETED.
```

## Development

This project follows **Spec-Driven Development**. Please refer to `Constitution.md` before contributing.
