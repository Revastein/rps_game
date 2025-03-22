import { ref, watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const username = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const errorMessage = ref('');
    const registrationSuccess = ref(false);
    const loading = ref(false);
    const router = useRouter();

    const usernameRegex = /^[a-zA-Z0-9]{0,16}$/; // Макс. 16 символов, только буквы и цифры
    const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()-_=+{};:,<.>?]*$/; // Только разрешённые символы, без ограничения длины

    // ✅ Автоматически очищаем лишние символы при вводе
    watch(username, (newValue) => {
      username.value = newValue.replace(/[^a-zA-Z0-9]/g, '').slice(0, 16);
    });

    watch(password, (newValue) => {
      password.value = newValue.replace(/[^a-zA-Z0-9!@#$%^&*()-_=+{};:,<.>?]/g, '');
    });

    watch(confirmPassword, (newValue) => {
      confirmPassword.value = newValue.replace(/[^a-zA-Z0-9!@#$%^&*()-_=+{};:,<.>?]/g, '');
    });

    const register = async () => {
      if (!username.value.trim()) {
        errorMessage.value = "Please enter a username.";
        return;
      }

      if (!usernameRegex.test(username.value)) {
        errorMessage.value = "Username can only contain letters and numbers (max 16 characters).";
        return;
      }

      if (password.value.length < 8 || !passwordRegex.test(password.value)) {
        errorMessage.value = "Password must be at least 8 characters long and contain only letters, numbers, and special characters.";
        return;
      }

      if (password.value !== confirmPassword.value) {
        errorMessage.value = "Passwords do not match.";
        return;
      }

      loading.value = true;
      try {
        await axios.post("/register", {
          username: username.value,
          password: password.value,
        });

        registrationSuccess.value = true;
        errorMessage.value = "";

        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } catch (error) {
        if (error.response?.status === 409) {
          errorMessage.value = "Username already exists. Choose another one.";
        } else {
          errorMessage.value = "An error occurred. Please try again.";
        }
      } finally {
        loading.value = false;
      }
    };

    const goToLogin = () => {
      router.push('/login');
    };

    return {
      username,
      password,
      confirmPassword,
      registrationSuccess,
      register,
      errorMessage,
      loading,
      goToLogin
    };
  }
};
