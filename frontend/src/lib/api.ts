import { authClient } from "./auth-client";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
    // Better Auth with jwtClient plugin usually provides the token via a specific method
    // or it's included in the session.
    // Let's try to get it using the standard ways.
    let token: string | undefined;
    
    try {
        // @ts-ignore - jwtClient adds this method
        const res = await authClient.getJWT?.();
        if (res && typeof res === 'object' && 'token' in res) {
            token = res.token as string;
        } else if (typeof res === 'string') {
            token = res;
        }
    } catch (e) {
        console.error("Error getting JWT:", e);
    }

    const headers = new Headers(options.headers);
    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }
    headers.set("Content-Type", "application/json");

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        if (response.status === 401) {
            // Handle unauthorized - maybe redirect to login
        }
        const error = await response.json().catch(() => ({ detail: "An error occurred" }));
        throw new Error(error.detail || "API request failed");
    }

    if (response.status === 204) return null;
    return response.json();
}

export interface Task {
    id: number;
    title: string;
    description?: string;
    status: 'PENDING' | 'COMPLETED';
    created_at: string;
    updated_at: string;
}

export const api = {
    getTasks: (): Promise<Task[]> => fetchWithAuth("/tasks"),
    getTask: (id: number): Promise<Task> => fetchWithAuth(`/tasks/${id}`),
    createTask: (task: { title: string; description?: string }): Promise<Task> => 
        fetchWithAuth("/tasks", {
            method: "POST",
            body: JSON.stringify(task),
        }),
    updateTask: (id: number, task: Partial<{ title: string; description: string; status: string }>): Promise<Task> =>
        fetchWithAuth(`/tasks/${id}`, {
            method: "PATCH",
            body: JSON.stringify(task),
        }),
    deleteTask: (id: number): Promise<{ ok: boolean }> =>
        fetchWithAuth(`/tasks/${id}`, {
            method: "DELETE",
        }),
    toggleTask: (id: number): Promise<Task> =>
        fetchWithAuth(`/tasks/${id}/toggle`, {
            method: "PATCH",
        }),
};
