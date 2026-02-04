# Todo App Monorepo

This project is a full-stack Todo application using FastAPI and Next.js.

## Structure

- `/backend`: FastAPI (Python 3.13+)
- `/frontend`: Next.js 16+ (TypeScript, Tailwind)
- `/specs`: Organized project specifications
- `.spec-kit`: Configuration for Spec-Driven Development

## Prerequisites

- Python 3.13+ and `uv`
- Node.js 18+ and `npm`

## Setup

### Backend
```bash
cd backend
uv sync
```

### Frontend
```bash
cd frontend
npm install
```

## Running the Application

### Backend
```bash
cd backend
uv run fastapi dev src/todo_app/main.py
```

### Frontend
```bash
cd frontend
npm run dev
```

## Spec-Driven Development
Refer to `Constitution.md` and the `specs/` folder.
- `specs/features/`: Feature descriptions
- `specs/api/`: API endpoints and models
- `specs/database/`: Schema and persistence
- `specs/ui/`: UI components and design