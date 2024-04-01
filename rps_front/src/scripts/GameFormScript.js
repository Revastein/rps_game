import axios from 'axios';
import {userId} from '@/scripts/LoginFormScript';
import {useRouter} from 'vue-router';
import {ref, onMounted, onBeforeUnmount} from 'vue';

export const inLobby = ref(false);
export const lobbyId = ref('');
export const players = ref([]);
export const userPosition = ref(-1);

export default {
    setup() {
        const searching = ref(false);
        const userInQueue = ref(false);
        const userStat = ref({});
        const topPlayers = ref([]);
        const queueLength = ref(0);
        const router = useRouter();
        let lobbyInterval;
        let queueCheckInterval;

        const enterQueue = async () => {
            try {
                searching.value = true;
                const response = await axios.post("/join_queue", {user_id: userId.value});
                console.log(response.data);
                userInQueue.value = true;

                lobbyInterval = setInterval(async () => {
                    try {
                        const lobbyResponse = await axios.get(`/get_lobby_by_user/${userId.value}`);
                        const lobby = lobbyResponse.data;
                        if (lobby) {
                            clearInterval(lobbyInterval.value);
                            lobbyId.value = lobby.lobby_id;
                            inLobby.value = true;
                            players.value = lobby.players;
                            console.log("Fetched lobby information:", lobby);
                            await router.push({name: 'Lobby', params: {lobbyId: lobbyId.value}});
                        }
                    } catch (error) {
                        if (error.response && error.response.status === 404) {
                            console.log("Lobby not found, continuing search...");
                        }
                    }
                }, 1000);

                queueCheckInterval = setInterval(getQueueLength, 5000);

            } catch (error) {
                if (error.response.status === 400 && error.response.data.detail === "User already in the queue") {
                    console.error("User already in the queue");
                } else {
                    console.error(error);
                }
            } finally {
                searching.value = false;
            }
        };

        const cancelQueue = async () => {
            try {
                clearInterval(lobbyInterval);
                clearInterval(queueCheckInterval);
                await axios.delete("/delete_user_from_queue", {data: {user_id: userId.value}});
                userInQueue.value = false;
                await getQueueLength();
            } catch (error) {
                console.error(error);
            }
        };

        const getUserStat = async () => {
            try {
                const response = await axios.get(`/user/${userId.value}`);
                userStat.value = response.data;
                await getUserPosition();
            } catch (error) {
                console.error("Failed to fetch user stat:", error);
                throw error;
            }
        };

        const getQueueLength = async () => {
            try {
                const response = await axios.get("/get_queue");
                queueLength.value = response.data.length;
            } catch (error) {
                console.error("Failed to fetch queue length:", error);
            }
        };

        const fetchLobbyInfo = async () => {
            try {
                const lobbyResponse = await axios.get(`/get_lobby_by_user/${userId.value}`);
                const lobby = lobbyResponse.data;
                if (lobby) {
                    lobbyId.value = lobby.lobby_id;
                    inLobby.value = true;
                    players.value = lobby.players;
                    console.log("Fetched lobby information:", lobby);
                }
            } catch (error) {
                console.error("Failed to fetch lobby information:", error);
            }
        };

        const returnToLobby = async () => {
            try {
                if (lobbyId.value) {
                    await router.push({name: 'Lobby', params: {lobbyId: lobbyId.value}});
                    console.log("Returned to lobby:", lobbyId.value);
                } else {
                    console.error("No lobby ID found. Cannot return to lobby.");
                }
            } catch (error) {
                console.error("Failed to return to lobby:", error);
            }
        };

        const getUserPosition = async () => {
            try {
                const response = await axios.get("/users");
                const sortedPlayers = response.data.sort((a, b) => b.rating - a.rating);
                const userIndex = sortedPlayers.findIndex(player => player.user_id === userId.value);
                userPosition.value = userIndex !== -1 ? userIndex + 1 : -1;
            } catch (error) {
                console.error("Failed to get user position:", error);
            }
        };

        const getTopPlayers = async () => {
            try {
                const response = await axios.get("/users");
                const sortedPlayers = response.data.sort((a, b) => b.rating - a.rating);
                topPlayers.value = sortedPlayers.slice(0, 10);
            } catch (error) {
                console.error("Failed to get top players:", error);
            }
        };

        onMounted(async () => {
            try {
                await getTopPlayers();
                await getUserStat();
                await getQueueLength();
                if (!lobbyId.value) {
                    await fetchLobbyInfo();
                }
            } catch (error) {
                console.error("Failed to fetch user stat:", error);
            }
        });

        onBeforeUnmount(async () => {
            await cancelQueue();
            inLobby.value = false
        });

        const checkAndRedirect = async () => {
            try {
                if (!inLobby.value) {
                    await router.push('/game');
                }
            } catch (error) {
                console.error('Failed to redirect to game page:', error);
            }
        };

        return {
            searching,
            userInQueue,
            enterQueue,
            cancelQueue,
            userStat,
            queueLength,
            lobbyId,
            inLobby,
            checkAndRedirect,
            players,
            returnToLobby,
            userPosition,
            topPlayers,
        };
    }
};
