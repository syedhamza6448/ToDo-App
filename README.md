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

## Development

This project follows **Spec-Driven Development**. Please refer to `Constitution.md` before contributing.
