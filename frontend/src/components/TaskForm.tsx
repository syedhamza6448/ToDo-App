"use client";

import { useState } from "react";
import { api } from "@/lib/api";

interface TaskFormProps {
    onTaskCreated: () => void;
}

export default function TaskForm({ onTaskCreated }: TaskFormProps) {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim()) return;

        setLoading(true);
        setError("");
        try {
            await api.createTask({ title, description });
            setTitle("");
            setDescription("");
            onTaskCreated();
        } catch (err: any) {
            setError(err.message || "Failed to create task");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="p-6 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl shadow-sm space-y-4">
            <h2 className="text-lg font-bold text-zinc-900 dark:text-zinc-100">Add New Task</h2>
            {error && <p className="text-sm text-red-500">{error}</p>}
            <div className="space-y-3">
                <input
                    className="w-full px-4 py-3 bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-zinc-400"
                    placeholder="What needs to be done?"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                />
                <textarea
                    className="w-full px-4 py-3 bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-zinc-400 resize-none"
                    placeholder="Add a description (optional)"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={2}
                />
            </div>
            <button
                type="submit"
                disabled={loading || !title.trim()}
                className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-500/20"
            >
                {loading ? "Creating..." : "Add Task"}
            </button>
        </form>
    );
}
