import {ref} from 'vue';
import axios from 'axios';
import {useRouter} from 'vue-router';

export const userId = ref(null);
export const username = ref(null)

export default {
    setup() {
        const username = ref('');
        const password = ref('');
        const errorMessage = ref('');
        const loginSuccess = ref(false);
        const router = useRouter();

        const login = async () => {
            try {
                const response = await axios.post("/login", {
                    username: username.value,
                    password: password.value
                });
                console.log(response.data);
                userId.value = response.data.user_id;
                loginSuccess.value = true;
                username.value = response.data.username;

                localStorage.setItem('userId', response.data.user_id);
                localStorage.setItem('username', response.data.username)

                await router.push('/game');
            } catch (error) {
                console.error(error);
                if (error.response) {
                    if (error.response.status === 401) {
                        errorMessage.value = "Incorrect username or password.";
                    } else if (error.response.status === 404) {
                        errorMessage.value = "Username not found."
                    }
                    else {
                        errorMessage.value = "An error occurred while trying to login. Please try again later.";
                    }
                } else {
                    errorMessage.value = "An error occurred. Please check your internet connection and try again.";
                }
            }
        };

        return {username, password, loginSuccess, login, errorMessage};
    }
};