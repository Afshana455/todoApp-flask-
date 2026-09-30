import { setTokens, clearTokens} from "./api";

export async function login(email, password) {
    const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password})
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.message || "Login failed"
        );
    }
    setTokens(data.access_token,  data.refresh_token);
    return data;
}

export async function register(name, email, password) {
    const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ name, email, password})
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(  data.message);
    }
    return data;
}

export function logout() {
    clearTokens();
}