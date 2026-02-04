"use client";

import { useEffect, useState } from "react";
import { Task, api } from "@/lib/api";
import TaskItem from "./TaskItem";

interface TaskListProps {
    refreshTrigger: number;
    onRefresh: () => void;
}

export default function TaskList({ refreshTrigger, onRefresh }: TaskListProps) {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const fetchTasks = async () => {
        try {
            const data = await api.getTasks();
            setTasks(data);
        } catch (err: any) {
            setError(err.message || "Failed to fetch tasks");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTasks();
    }, [refreshTrigger]);

    if (loading) {
        return (
            <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="h-24 bg-zinc-100 dark:bg-zinc-800 animate-pulse rounded-xl" />
                ))}
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-4 text-center text-red-500 bg-red-50 dark:bg-red-900/10 rounded-xl border border-red-200 dark:border-red-800">
                {error}
                <button onClick={fetchTasks} className="ml-4 underline">Retry</button>
            </div>
        );
    }

    if (tasks.length === 0) {
        return (
            <div className="text-center py-12 px-4 border-2 border-dashed border-zinc-200 dark:border-zinc-800 rounded-2xl">
                <p className="text-zinc-500 dark:text-zinc-400">No tasks yet. Create one above!</p>
            </div>
        );
    }

    // Separate pending and completed tasks
    const pendingTasks = tasks.filter(t => t.status === 'PENDING');
    const completedTasks = tasks.filter(t => t.status === 'COMPLETED');

    return (
        <div className="space-y-8">
            {pendingTasks.length > 0 && (
                <div className="space-y-4">
                    <h3 className="text-sm font-semibold text-zinc-500 uppercase tracking-wider">Active Tasks</h3>
                    <div className="grid gap-3">
                        {pendingTasks.map((task) => (
                            <TaskItem 
                                key={task.id} 
                                task={task} 
                                onUpdate={onRefresh} 
                                onDelete={onRefresh} 
                            />
                        ))}
                    </div>
                </div>
            )}

            {completedTasks.length > 0 && (
                <div className="space-y-4">
                    <h3 className="text-sm font-semibold text-zinc-500 uppercase tracking-wider">Completed</h3>
                    <div className="grid gap-3">
                        {completedTasks.map((task) => (
                            <TaskItem 
                                key={task.id} 
                                task={task} 
                                onUpdate={onRefresh} 
                                onDelete={onRefresh} 
                            />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
