"use client";

import { useEffect, useRef, useState } from "react";
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import Script from "next/script";
import Navbar from "@/components/Navbar";
import type { OpenAIChatKit } from "@openai/chatkit";

export default function ChatPage() {
    const { data: session, isPending } = useSession();
    const router = useRouter();
    const chatkitRef = useRef<OpenAIChatKit>(null);
    const [isScriptLoaded, setIsScriptLoaded] = useState(false);

    useEffect(() => {
        if (!isPending && !session) {
            router.push("/auth/signin");
        }
    }, [session, isPending, router]);

    useEffect(() => {
        if (isScriptLoaded && chatkitRef.current && session?.user?.id) {
            const dk = process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || "dk-placeholder";
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            
            chatkitRef.current.setOptions({
                api: {
                    url: `${apiUrl}/api/chatkit`,
                    domainKey: dk,
                },
                theme: "light",
                header: {
                    title: {
                        text: "ToDo Assistant"
                    }
                }
            });

            const errorHandler = (event: any) => {
                console.error("ChatKit Error:", event.detail.error);
            };

            chatkitRef.current.addEventListener("chatkit.error", errorHandler);
            
            return () => {
                if (chatkitRef.current) {
                    chatkitRef.current.removeEventListener("chatkit.error", errorHandler);
                }
            };
        }
    }, [isScriptLoaded, session]);

    if (isPending) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-zinc-50 dark:bg-zinc-950">
                <div className="animate-spin h-8 w-8 border-4 border-blue-600 border-t-transparent rounded-full" />
            </div>
        );
    }

    if (!session) return null;

    return (
        <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex flex-col">
            <Navbar />
            <Script 
                src="https://cdn.openai.com/chatkit/v1/index.js" 
                onLoad={() => setIsScriptLoaded(true)}
            />
            
            <main className="flex-1 flex flex-col max-w-5xl mx-auto w-full px-4 py-8">
                <div className="mb-4">
                    <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">AI Assistant</h1>
                    <p className="text-zinc-500 dark:text-zinc-400">Powered by OpenAI ChatKit</p>
                </div>
                
                <div className="flex-1 border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden bg-white shadow-xl min-h-[600px]">
                    {/* @ts-ignore - openai-chatkit is a custom element */}
                    <openai-chatkit 
                        ref={chatkitRef} 
                        style={{ width: '100%', height: '100%', display: 'block' }}
                    />
                </div>
            </main>
        </div>
    );
}

