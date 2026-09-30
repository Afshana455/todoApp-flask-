let accessToken = sessionStorage.getItem("accessToken");
let refreshToken = sessionStorage.getItem("refreshToken");

let refreshPromise = null;

export function setTokens(access, refresh) {
    accessToken = access;
    refreshToken = refresh;

    sessionStorage.setItem("accessToken", access);
    sessionStorage.setItem("refreshToken", refresh);
}

export function clearTokens() {
    accessToken = null;
    refreshToken = null;

    sessionStorage.removeItem("accessToken");
    sessionStorage.removeItem("refreshToken");
}

export function getAccessToken() {
    return accessToken;
}

async function refreshAccessToken() {
    if (!refreshPromise) {
        refreshPromise = (async () => {
            try {
                const response = await fetch("/api/auth/refresh", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${refreshToken}`
                    }
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.message || "Session expired"
                    );
                }

                accessToken = data.access_token;

                sessionStorage.setItem(
                    "accessToken",
                    accessToken
                );

                return accessToken;
            } finally {
                refreshPromise = null;
            }
        })();
    }
    return await refreshPromise;
}

export async function apiRequest(url, options = {}) {
    const headers = {"Authorization": `Bearer ${accessToken}`, "Content-Type": "application/json"};

    let response = await fetch(url, { ...options, headers});

    if (response.status !== 401) {
        return response;
    }

    const newToken = await refreshAccessToken();

    const retryHeaders = {
        "Authorization": `Bearer ${newToken}`,
        "Content-Type": "application/json"
    };

    response = await fetch(url, {
        ...options,
        headers: retryHeaders
    });

    return response;
}