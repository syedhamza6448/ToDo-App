# Gemini Assistant Instructions

This file guides the AI assistant (Gemini) in working with this project.

## Project Context
- **Type**: Python CLI/Web Application (Todo App)
- **Toolchain**: `uv` for dependency management and environment handling.
- **Python Version**: 3.13+
- **Structure**:
    - `src/`: Source code.
    - `specs/`: Specifications (SDD).
    - `Constitution.md`: Development rules.

## Core Mandates
1.  **Follow the Constitution**: Adhere to Spec-Driven Development. Read `Constitution.md` if unsure.
2.  **Use `uv`**: Always use `uv` for package management (`uv add`, `uv run`, `uv sync`).
    - Run scripts: `uv run src/todo_app/main.py`
    - Add dependencies: `uv add <package>`
3.  **Source Layout**: Application code resides in `src/todo_app/`.
4.  **Testing**: (Future) Use `pytest` via `uv run pytest`.

## Common Commands
- **Run App**: `uv run src/todo_app/main.py`
- **Install/Sync**: `uv sync`
- **Lint/Format**: `uv run ruff check .` / `uv run ruff format .` (if installed)

## Tone & Style
- Be concise.
- Check specifications before implementing complex logic.
