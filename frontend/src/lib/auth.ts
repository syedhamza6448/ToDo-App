import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
    // In a real app, you'd use a database adapter here
    // For this prototype, we'll assume a database is configured in .env

    secret: process.env.BETTER_AUTH_SECRET || "HgIOp5ggpCchLw144gHptypq16wv1WKi",
    emailAndPassword: {
        enabled: true
    },
    plugins: [
        jwt()
    ]
});
