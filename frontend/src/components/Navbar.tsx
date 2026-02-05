"use client";

import { signOut, useSession } from "@/lib/auth-client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

export default function Navbar() {
    const { data: session, isPending } = useSession();
    const router = useRouter();
    const pathname = usePathname();

    const handleSignOut = async () => {
        await signOut({
            fetchOptions: {
                onSuccess: () => {
                    router.push("/auth/signin");
                },
            },
        });
    };

    return (
        <nav className="sticky top-0 z-10 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border-b border-zinc-200 dark:border-zinc-800">
            <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
                <div className="flex items-center gap-8">
                    <div className="flex items-center gap-2">
                        <div className="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center">
                            <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                            </svg>
                        </div>
                        <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400">
                            TaskMaster
                        </span>
                    </div>

                    {!isPending && session && (
                        <div className="hidden md:flex items-center gap-6">
                            <Link 
                                href="/dashboard" 
                                className={`text-sm font-medium transition-colors ${
                                    pathname === "/dashboard" 
                                        ? "text-blue-600 dark:text-blue-400" 
                                        : "text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100"
                                }`}
                            >
                                Dashboard
                            </Link>
                            <Link 
                                href="/chat" 
                                className={`text-sm font-medium transition-colors ${
                                    pathname === "/chat" 
                                        ? "text-blue-600 dark:text-blue-400" 
                                        : "text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100"
                                }`}
                            >
                                AI Assistant
                            </Link>
                        </div>
                    )}
                </div>

                <div className="flex items-center gap-4">
                    {!isPending && session && (
                        <>
                            <div className="hidden sm:block text-right">
                                <p className="text-sm font-medium text-zinc-900 dark:text-zinc-100">{session.user.name}</p>
                                <p className="text-xs text-zinc-500">{session.user.email}</p>
                            </div>
                            <button
                                onClick={handleSignOut}
                                className="px-4 py-2 text-sm font-semibold text-zinc-600 dark:text-zinc-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                            >
                                Sign Out
                            </button>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
}
