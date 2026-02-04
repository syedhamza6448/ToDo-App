"use client";

import { useEffect, useState } from "react";
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import TaskForm from "@/components/TaskForm";
import TaskList from "@/components/TaskList";

export default function Dashboard() {
    const { data: session, isPending } = useSession();
    const router = useRouter();
    const [refreshTrigger, setRefreshTrigger] = useState(0);

    const refreshTasks = () => setRefreshTrigger(prev => prev + 1);

    useEffect(() => {
        if (!isPending && !session) {
            router.push("/auth/signin");
        }
    }, [session, isPending, router]);

    if (isPending) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-zinc-50 dark:bg-zinc-950">
                <div className="animate-spin h-8 w-8 border-4 border-blue-600 border-t-transparent rounded-full" />
            </div>
        );
    }

    if (!session) return null;

    return (
        <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950">
            <Navbar />
            <main className="max-w-3xl mx-auto px-4 py-12 space-y-12">
                <section>
                    <TaskForm onTaskCreated={refreshTasks} />
                </section>

                <section className="space-y-6">
                    <div className="flex items-center justify-between px-2">
                        <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">Your Tasks</h2>
                        <button 
                            onClick={refreshTasks}
                            className="p-2 text-zinc-500 hover:text-blue-600 transition-colors"
                        >
                            <svg className={`h-5 w-5 ${refreshTrigger > 0 ? 'animate-spin-once' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                        </button>
                    </div>
                    <TaskList refreshTrigger={refreshTrigger} onRefresh={refreshTasks} />
                </section>
            </main>
        </div>
    );
}
