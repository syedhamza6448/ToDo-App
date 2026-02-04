import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
    // In a real app, you'd use a database adapter here
    // For this prototype, we'll assume a database is configured in .env
    database: {
        provider: "sqlite", // or "postgres"
        url: process.env.DATABASE_URL || "file:./auth.db"
    },
    emailAndPassword: {
        enabled: true
    },
    plugins: [
        jwt({
            jwt: {
                secret: process.env.BETTER_AUTH_SECRET || "a-very-secret-shared-key-12345"
            }
        })
    ]
});
