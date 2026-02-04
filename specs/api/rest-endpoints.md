# Specification: REST API Endpoints

## 1. Overview
This document defines the RESTful API for the Todo application. All endpoints require authentication (provided via headers/Better Auth) and ensure user-scoped data access.

## 2. Base URL
`/api/v1`

## 3. Data Models (Pydantic)

### 3.1. TaskCreate
- `title`: String (Required)
- `description`: String (Optional)

### 3.2. TaskUpdate
- `title`: String (Optional)
- `description`: String (Optional)
- `status`: Enum (PENDING, COMPLETED) (Optional)

### 3.3. TaskRead
- `id`: Integer
- `title`: String
- `description`: String
- `status`: Enum
- `created_at`: DateTime
- `updated_at`: DateTime

## 4. Endpoints

### 4.1. Tasks Management

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/tasks` | List all tasks for the authenticated user. | Yes |
| `POST` | `/tasks` | Create a new task for the authenticated user. | Yes |
| `GET` | `/tasks/{id}` | Get details of a specific task. | Yes |
| `PUT` | `/tasks/{id}` | Replace/Update task details. | Yes |
| `PATCH` | `/tasks/{id}` | Partially update task details. | Yes |
| `DELETE` | `/tasks/{id}` | Remove a task. | Yes |
| `PATCH` | `/tasks/{id}/toggle` | Toggle completion status. | Yes |

## 5. Security & Scoping
- **Mandatory Filter**: Every query to the database MUST include `.where(Task.user_id == current_user_id)`.
- **Ownership Check**: If a user attempts to access an ID that does not belong to them, the system must return a `404 Not Found` to avoid leaking task existence.

## 6. Error Handling

| Status Code | Description |
| :--- | :--- |
| `200` | Success. |
| `201` | Created successfully. |
| `400` | Bad Request (Validation error). |
| `401` | Unauthorized (Missing/Invalid token). |
| `404` | Not Found (ID doesn't exist or doesn't belong to user). |
| `500` | Internal Server Error. |
