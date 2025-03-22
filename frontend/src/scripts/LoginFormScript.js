import { ref, watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { createWebSocket, closeWebSocket } from "@/websocket/ws";

export default {
  setup() {
    const username = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const loginSuccess = ref(false);
    const loading = ref(false);
    const router = useRouter();

    const usernameRegex = /^[a-zA-Z0-9]{1,16}$/;
    const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()-_=+{};:,<.>?]*$/;

    watch(username, (newValue) => {
      username.value = newValue.replace(/[^a-zA-Z0-9]/g, '').slice(0, 16);
    });

    watch(password, (newValue) => {
      password.value = newValue.replace(/[^a-zA-Z0-9!@#$%^&*()-_=+{};:,<.>?]/g, '');
    });

    const login = async () => {
      errorMessage.value = '';

      if (!username.value.trim()) {
        errorMessage.value = 'Please enter a username.';
        return;
      }

      if (!usernameRegex.test(username.value)) {
        errorMessage.value = 'Username can only contain letters and numbers (max 16 characters).';
        return;
      }

      if (!passwordRegex.test(password.value)) {
        errorMessage.value = 'Password contains invalid characters.';
        return;
      }

      loading.value = true;

      try {
        const formData = new URLSearchParams();
        formData.append('username', username.value);
        formData.append('password', password.value);

        const response = await axios.post('/login', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        const accessToken = response.data.access_token;
        const userId = response.data.user_id;

        if (accessToken) {
          localStorage.setItem('access_token', accessToken);
          localStorage.setItem('user_id', userId);
          loginSuccess.value = true;
          errorMessage.value = '';

          console.log("✅ Login successful! Connecting WebSocket...");
          createWebSocket(); // ✅ Подключаем WebSocket

          setTimeout(() => {
            router.push('/game');
          }, 2000);
        } else {
          errorMessage.value = 'Error retrieving token. Please try again.';
        }
      } catch (error) {
        if (error.response?.status === 401) {
          errorMessage.value = 'Invalid username or password.';
        } else {
          errorMessage.value = 'An error occurred. Please try again.';
        }
      } finally {
        loading.value = false;
      }
    };

    const goToRegister = () => {
      router.push('/register');
    };

    return { username, password, loginSuccess, login, errorMessage, loading, goToRegister };
  }
};
