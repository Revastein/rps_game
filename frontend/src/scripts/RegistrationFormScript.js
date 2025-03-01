import {ref} from 'vue';
import axios from 'axios';
import {useRouter} from 'vue-router';

export default {
    setup() {
        const username = ref('');
        const password = ref('');
        const errorMessage = ref('');
        const registrationSuccess = ref(false);
        const router = useRouter();

        const register = async () => {
            try {
                if (!username.value) {
                    errorMessage.value = "Please enter a username.";
                    return;
                }

                if (password.value.length < 8) {
                    errorMessage.value = "Password must be at least 8 characters long.";
                    return;
                }

                const response = await axios.post("/register", {
                    username: username.value,
                    password: password.value
                });
                console.log(response.data);
                registrationSuccess.value = true;
                setTimeout(async () => {
                    await router.push('/login');
                }, 2000);
            } catch (error) {
                console.error(error);
                if (error.response) {
                    if (error.response.status === 409) {
                        errorMessage.value = "Username already exists. Please choose another one.";
                    } else {
                        errorMessage.value = "An error occurred while trying to register. Please try again later.";
                    }
                } else {
                    errorMessage.value = "An error occurred. Please check your internet connection and try again.";
                }
            }
        };

        return {username, password, registrationSuccess, register, errorMessage};
    }
};
