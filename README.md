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

## Environment Variables

### Shared Secrets
Both `/frontend` and `/backend` must share the same `BETTER_AUTH_SECRET` for JWT verification.

### Backend (.env)
- `DATABASE_URL`: Neon PostgreSQL connection string.
- `BETTER_AUTH_SECRET`: Shared secret for JWT.

### Frontend (.env.local)
- `DATABASE_URL`: Database connection for Better Auth.
- `BETTER_AUTH_SECRET`: Shared secret for JWT.
- `NEXT_PUBLIC_APP_URL`: e.g., `http://localhost:3000`

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