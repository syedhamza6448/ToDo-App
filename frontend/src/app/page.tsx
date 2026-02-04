"use client";

import { useEffect } from "react";
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

export default function Home() {
    const { data: session, isPending } = useSession();
    const router = useRouter();

    useEffect(() => {
        if (!isPending) {
            if (session) {
                router.push("/dashboard");
            } else {
                router.push("/auth/signin");
            }
        }
    }, [session, isPending, router]);

    return (
        <div className="flex items-center justify-center min-h-screen bg-zinc-50 dark:bg-zinc-950">
            <div className="animate-spin h-8 w-8 border-4 border-blue-600 border-t-transparent rounded-full" />
        </div>
    );
}