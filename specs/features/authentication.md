# Specification: Authentication (Better Auth)

## 1. Overview
This project uses **Better Auth** for user management and authentication. The frontend (Next.js) handles the login/signup UI and session management, while the backend (FastAPI) verifies identity using shared JWT secrets.

## 2. Technical Stack
- **Frontend**: Better Auth with JWT Plugin.
- **Backend**: FastAPI with JWT verification (using `PyJWT`).
- **Shared Secret**: `BETTER_AUTH_SECRET` used by both for signing and verifying tokens.

## 3. Authentication Flow
1. User signs up/in via Next.js UI.
2. Better Auth generates a session and a JWT.
3. Frontend attaches the JWT to the `Authorization: Bearer <token>` header for API requests.
4. Backend verifies the JWT using the shared `BETTER_AUTH_SECRET`.
5. Backend extracts `user_id` (sub) from the token to scope database queries.

## 4. JWT Structure
The JWT should contain:
- `sub`: User ID (Foreign key for Tasks).
- `email`: User email.
- `exp`: Expiration timestamp.

## 5. Security Mandates
- **No Anonymous Access**: All `/tasks` endpoints must return `401 Unauthorized` if no valid token is present.
- **Token Validation**: Backend must check signature, expiration, and issuer.
- **HTTPS**: Required for all production traffic.

## 6. UI Requirements
- `/signup`: Email, Password, Name.
- `/signin`: Email, Password.
- `/logout`: Clears session and redirects to home.
- **Protected Routes**: Redirect unauthenticated users from `/dashboard` to `/signin`.
