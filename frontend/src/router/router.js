import { createRouter, createWebHistory } from 'vue-router';
import RegisterView from '@/views/RegisterView.vue';
import LoginView from '@/views/LoginView.vue';
import MainMenuView from "@/views/MainMenuView.vue";

const routes = [
  { path: '/register', component: RegisterView },
  { path: '/login', component: LoginView },
  { path: '/game', component: MainMenuView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;