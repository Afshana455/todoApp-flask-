import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import TodoView from "../views/TodoView.vue";

const router = createRouter({
    history: createWebHistory(),

    routes: [
        {
            path: "/login",
            component: LoginView
        },
        {
            path: "/register",
            component: RegisterView
        },
        {
            path: "/todos",
            component: TodoView,
            meta: {
                requiresAuth: true
            }
        }
    ]
});

router.beforeEach((to) => {
    const accessToken = sessionStorage.getItem(
        "accessToken"
    );

    if (to.meta.requiresAuth && !accessToken) {
        return "/login";
    }

    if (
        (to.path === "/login" || to.path === "/register") &&
        accessToken
    ) {
        return "/todos";
    }
});

export default router;