<template>
    <div>
        <h1>Register</h1>
        <form @submit.prevent="handleRegister">
            <div>
                <label>Name</label>
                <input  type="text"  v-model="name"  required >
            </div>
            <div>
                <label>Email</label>
                <input type="email" v-model="email" required>
            </div>
            <div>
                <label>Password</label>
                <input type="password"  v-model="password" required>
           </div>

            <button type="submit">Register </button>
        </form>

        <p v-if="message"> {{ message }}</p>

        <p v-if="errorMessage"> {{ errorMessage }} </p>

        <p> Already have an account?
            <router-link to="/login"> Login </router-link>
        </p>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { register } from "../api/auth";

const name = ref("");
const email = ref("");
const password = ref("");
const confirm_password = ref("")

const message = ref("");
const errorMessage = ref("");

const router = useRouter();

async function handleRegister() {
    message.value = "";
    errorMessage.value = "";

    try {

        await register( name.value, email.value, password.value);

        message.value = "Registration successful";

        setTimeout(() => { router.push("/login"); }, 1000);
    } 
    catch (error) {
        errorMessage.value = error.message;
    }
}
</script>