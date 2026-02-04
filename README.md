# ToDo App - Full Stack Deployment Guide

This guide outlines the steps to deploy the full-stack ToDo application, including connecting the frontend and backend, setting up environment variables, and deploying to production environments.

## 1. Environment Variables Setup

Both the frontend (Next.js) and backend (FastAPI) require specific environment variables.

### Backend (`backend/.env`)

Create a `.env` file in the `backend/` directory with the following content. These variables will be loaded by `python-dotenv`.

```env
BETTER_AUTH_SECRET=HgIOp5ggpCchLw144gHptypq16wv1WKi
DATABASE_URL=sqlite:///./prod.db # Or your production database URL (e.g., PostgreSQL connection string)
```

**Note:** For production deployments, `DATABASE_URL` should point to a persistent database instance (e.g., a managed PostgreSQL service).

### Frontend (`frontend/.env.local`)

Create a `.env.local` file in the `frontend/` directory with the following content. These variables are picked up by Next.js.

```env
NEXT_PUBLIC_API_URL=<YOUR_DEPLOYED_BACKEND_URL>
BETTER_AUTH_SECRET=HgIOp5ggpCchLw144gHptypq16wv1WKi
```

**Note:** Replace `<YOUR_DEPLOYED_BACKEND_URL>` with the actual URL of your deployed backend service.

## 2. Backend Deployment (FastAPI)

Here are common options for deploying the FastAPI backend. Render is recommended for its ease of use.

### Choosing a Hosting Platform

*   **Render (Recommended):** Managed platform for web apps, databases, and more. Excellent for Python applications.
*   **Fly.io:** Offers global distribution and autoscaling, good for geographically dispersed users.
*   **Google Cloud Run / AWS App Runner:** Serverless container platforms from major cloud providers.
*   **Heroku:** Popular PaaS, but check their current free tier limitations.

### General Preparation Steps

1.  **Database:** For production, use a persistent database. Most platforms offer managed PostgreSQL, MySQL, or other options. Update your `DATABASE_URL` environment variable accordingly.
2.  **Dependencies:** Ensure all your Python dependencies are listed in `backend/pyproject.toml`.
3.  **Entry Point:** The command to run your FastAPI application will typically be:
    `uvicorn todo_app.main:app --host 0.0.0.0 --port $PORT`
    (Adjust `$PORT` to the environment variable your hosting platform uses for the port).

### Example Deployment: Render

1.  **Sign up/Log in:** Go to [render.com](https://render.com/).
2.  **New Web Service:** Connect your GitHub/GitLab repository where your code is hosted.
3.  **Configuration:**
    *   **Root Directory:** `backend`
    *   **Runtime:** Python 3
    *   **Build Command:** `uv sync`
    *   **Start Command:** `uvicorn todo_app.main:app --host 0.0.0.0 --port $PORT`
    *   **Environment Variables:** Add `BETTER_AUTH_SECRET` and `DATABASE_URL` with your production values.
4.  **Deploy:** Render will build and deploy your application. Make a note of the public URL assigned to your backend service; you'll need it for the frontend.

## 3. Frontend Deployment (Next.js to Vercel)

Vercel is the recommended platform for Next.js applications.

1.  **Sign up/Log in:** Go to [vercel.com](https://vercel.com/) and connect your GitHub/GitLab/Bitbucket account.
2.  **Import Git Repository:** Select the repository containing your frontend code.
3.  **Configure Project:**
    *   **Root Directory:** `frontend`
    *   **Framework Preset:** Next.js
    *   **Build & Output Settings:** Vercel usually auto-detects these, but ensure the "Build Command" is `npm run build` and "Output Directory" is `.next`.
    *   **Environment Variables:** Add the following:
        *   `NEXT_PUBLIC_API_URL`: Set this to the public URL of your deployed backend service.
        *   `BETTER_AUTH_SECRET`: Use the same secret as your backend.
4.  **Deploy:** Vercel will build and deploy your Next.js application.

## 4. Testing CRUD Operations with Authentication

After both frontend and backend are deployed:

1.  **Access Frontend:** Open your deployed frontend application URL.
2.  **Sign Up:** Create a new user account. This should interact with your deployed backend.
3.  **Sign In:** Log in with the newly created account.
4.  **Create Task:** Add new tasks using the task form.
5.  **Read Tasks:** Verify that your tasks appear in the list.
6.  **Update Task:** Edit an existing task's title, description, or toggle its status.
7.  **Delete Task:** Remove a task.
8.  **Logout:** Ensure session termination works correctly.

This confirms the full integration and functionality of your deployed application.
