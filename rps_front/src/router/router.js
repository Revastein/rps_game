import {createRouter, createWebHistory} from 'vue-router';
import {userId} from '@/scripts/LoginFormScript';
import LoginForm from '@/components/LoginForm.vue';
import RegistrationForm from '@/components/RegistrationForm.vue';
import GameForm from "@/components/GameForm.vue";
import LobbyForm from "@/components/GameLobbyForm.vue";

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginForm
    },
    {
        path: '/register',
        name: 'Register',
        component: RegistrationForm
    },
    {
        path: '/game',
        name: 'Game',
        component: GameForm
    },
    {
        path: '/lobby/:lobbyId',
        name: 'Lobby',
        component: LobbyForm
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    if (to.name !== 'Login' && to.name !== 'Register' && !userId.value) {
        next('/login');
    } else if ((to.name === 'Login' || to.name === 'Register') && userId.value) {
        next('/game');
    } else {
        next();
    }
});

export default router;
