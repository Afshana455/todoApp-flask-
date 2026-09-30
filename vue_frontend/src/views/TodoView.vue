<template>
    <div>
        <header>
            <h1>My Todos</h1>
            <button @click="handleLogout"> Logout </button>
        </header>

        <main>
            <section>
                <input type="text" v-model="searchText" placeholder="Search todos...">
                <button @click="openCreateForm"> + </button>
            </section>

            <section v-if="showForm">
                <h2>
                    {{ editingTodo ? "Edit Todo" : "Add Todo" }}
                </h2>

                <form @submit.prevent="handleSubmit">
                    <div>
                        <label for="title"> Title </label>

                        <input id="title" type="text" v-model="form.title" required>
                    </div>

                    <div>
                        <label for="description">
                            Description
                        </label>

                        <textarea
                            id="description"
                            v-model="form.description"
                        ></textarea>
                    </div>

                    <div v-if="editingTodo">
                        <label>
                            <input type="checkbox" v-model="form.completed">
                            Completed
                        </label>
                    </div>

                    <button type="submit" :disabled="saving">
                        {{ saving ? "Saving..." : "Save" }}
                    </button>

                    <button type="button" @click="closeForm">
                        Cancel
                    </button>
                </form>
            </section>

            <p v-if="loading">
                Loading todos...
            </p>

            <p v-if="errorMessage">
                {{ errorMessage }}
            </p>

            <section>
                <p v-if="todos.length === 0 && !loading">
                    No todos found.
                </p>

                <article v-for="todo in todos" :key="todo.id">
                    <h2>{{ todo.title }}</h2>

                    <p>
                        {{ todo.description || "No description" }}
                    </p>

                    <label>
                        <input type="checkbox" :checked="Boolean(todo.completed)" @change="handleCompletion(todo)">
                        Completed
                    </label>

                    <button @click="openEditForm(todo)">
                        Edit
                    </button>

                    <button @click="handleDelete(todo.id)">
                        Delete
                    </button>

                    <hr>
                </article>
            </section>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted ,watch} from "vue";
import { refDebounced } from "@vueuse/core";
import { useRouter } from "vue-router";
import { getTodos, createTodo, updateTodo, deleteTodo} from "../api/todo";
import { logout } from "../api/auth";

const router = useRouter();

const todos = ref([]);
const searchText = ref("");
const debouncedSearch = refDebounced(searchText, 500);

const loading = ref(false);
const saving = ref(false);
const errorMessage = ref("");

const showForm = ref(false);
const editingTodo = ref(null);

const form = ref({ title: "", description: "", completed: false});



async function loadTodos(search = "") {
    loading.value = true;
    errorMessage.value = "";

    try {
        const data = await getTodos(search);
        todos.value = data.todos;
    } 
    catch (error) {
        errorMessage.value = error.message;
    } 
    finally {
        loading.value = false;
    }
}
watch(debouncedSearch, (search)=>{loadTodos(search)})

function resetForm() {
    form.value = { title: "", description: "", completed: false};
    editingTodo.value = null;
}

function openCreateForm() {
    resetForm();
    showForm.value = true;
}

function openEditForm(todo) {
    editingTodo.value = todo;

    form.value = { title: todo.title, description: todo.description || "", completed: Boolean(todo.completed)};
    showForm.value = true;
}

function closeForm() {
    showForm.value = false;
    resetForm();
}

async function handleSubmit() {
    saving.value = true;
    errorMessage.value = "";

    try {
        if (editingTodo.value) {
            await updateTodo( editingTodo.value.id, form.value.title, form.value.description, form.value.completed);
            const index = todos.value.findIndex( todo => todo.id === editingTodo.value.id );

            if (index !== -1) {
                todos.value[index] = {
                    ...todos.value[index],
                    title: form.value.title,
                    description: form.value.description,
                    completed: form.value.completed
                };
            }
        } else {
            const data = await createTodo( form.value.title, form.value.description);
            await loadTodos(debouncedSearch.value);
        }

        closeForm();
    } 
    catch (error) {
        errorMessage.value = error.message;
    } 
    finally {
        saving.value = false;
    }
}

async function handleCompletion(todo) {
    const newCompleted = !Boolean(todo.completed);

    try {
        await updateTodo( todo.id, todo.title, todo.description,  newCompleted);

        todo.completed = newCompleted;
    } 
    catch (error) {
        errorMessage.value = error.message;
    }
}

async function handleDelete(todoId) {
    errorMessage.value = "";

    try {
        await deleteTodo(todoId);
        todos.value = todos.value.filter( todo => todo.id !== todoId);
    }
     catch (error) {
        errorMessage.value = error.message;
    }
}

function handleLogout() {
    logout();
    router.push("/login");
}

onMounted(() => {loadTodos();});
</script>