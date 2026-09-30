<template>
    <div>
        <h1>Login</h1>

        <form @submit.prevent="handleLogin">
            <div>
                <label for="email">Email</label>
                <input id="email" type="email" v-model="email" required>
            </div>

            <div>
                <label for="password">Password</label>
                <input  id="password" type="password" v-model="password" required>
            </div>

            <button type="submit" :disabled="loading">
                {{ loading ? "Logging in..." : "Login" }}
            </button>
        </form>

        <p v-if="errorMessage">
            {{ errorMessage }}
        </p>

        <p>
            Don't have an account?
            <router-link to="/register">
                Register
            </router-link>
        </p>
    </div>
</template>

<script setup> 
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "../api/auth";

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false);

const router = useRouter();

async function handleLogin() {
    errorMessage.value = "";
    loading.value = true;

    try {
        await login( email.value, password.value );

        router.push("/todos");
    } 
    catch (error) { errorMessage.value = error.message;} 

    finally { loading.value = false;}
}
</script>