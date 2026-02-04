"use client";

import { useState } from "react";
import { signUp } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

export default function SignUp() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");
    const [error, setError] = useState("");
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        
        const { error: authError } = await signUp.email({
            email,
            password,
            name,
            callbackURL: "/dashboard"
        });

        if (authError) {
            setError(authError.message || "Failed to sign up");
        } else {
            router.push("/dashboard");
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen py-2">
            <h1 className="text-2xl font-bold mb-6">Sign Up</h1>
            <form onSubmit={handleSubmit} className="w-full max-w-xs space-y-4">
                {error && <p className="text-red-500 text-sm">{error}</p>}
                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-3 py-2 border rounded"
                    required
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-3 py-2 border rounded"
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-3 py-2 border rounded"
                    required
                />
                <button
                    type="submit"
                    className="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                    Sign Up
                </button>
            </form>
            <p className="mt-4 text-sm">
                Already have an account? <a href="/auth/signin" className="text-blue-600">Sign In</a>
            </p>
        </div>
    );
}
