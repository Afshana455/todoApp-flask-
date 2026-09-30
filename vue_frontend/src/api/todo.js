import { apiRequest } from "./api";

export async function getTodos(search = "") {
    const params = new URLSearchParams();
    if(search.trim()){
        params.set("search",search.trim());
    }
    const query = params.toString();
    const url = query ? `/api/todos/?${query}` : "/api/todos/";
    const response = await apiRequest(url);
    const data = await response.json();

    if (!response.ok) {
        throw new Error( data.message || "Failed to fetch todos");
    }

    return data;
}

export async function getTodo(todoId) {
    const response = await apiRequest(`/api/todos/${todoId}`);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(  data.message || "Failed to fetch todo");
    }

    return data;
}

export async function createTodo(title, description) {
    const response = await apiRequest("/api/todos/", {
        method: "POST",
        body: JSON.stringify({title, description})
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error( data.message || "Failed to create todo");
    }

    return data;
}

export async function updateTodo(todoId, title, description, completed) {
    const response = await apiRequest( `/api/todos/${todoId}`,
        {
            method: "PUT",
            body: JSON.stringify({ title, description, completed: Boolean(completed)})
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error( data.message || "Failed to update todo");
    }

    return data;
}

export async function deleteTodo(todoId) {
    const response = await apiRequest( `/api/todos/${todoId}`,
        {
            method: "DELETE"
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error( data.message || "Failed to delete todo");
    }

    return data;
}