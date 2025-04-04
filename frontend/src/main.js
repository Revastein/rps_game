import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import router from './router/router.js';

axios.defaults.baseURL = 'http://' + window.location.hostname + ':8000';

const app = createApp(App);
app.config.globalProperties.$axios = axios;
app.use(router);

app.mount('#app');
