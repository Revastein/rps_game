import axios from 'axios';
import {ref, computed, onMounted, onBeforeUnmount} from 'vue';
import {useRouter} from 'vue-router';
import {userId} from '@/scripts/LoginFormScript';
import {lobbyId, players} from '@/scripts/GameFormScript';

export default {
    setup() {
        const router = useRouter();
        let interval;
        const lobbyInterval = ref(null);
        const timerSeconds = 10;
        const timerCountdown = ref(timerSeconds);
        const winner = ref(null);
        const timerText = computed(() => `${timerCountdown.value} seconds left`);
        const timerVisible = ref(true);

        const handleLobbyResponse = async (lobbyResponse) => {
            const lobby = lobbyResponse.data;
            if (lobby) {
                lobbyId.value = lobby.lobby_id;
                players.value = lobby.players;
                await router.push({name: 'Lobby', params: {lobbyId: lobbyId.value}});
            }
        };

        const formattedPlayers = computed(() => {
            return players.value.map(player => {
                const playerId = player.user_id;
                let formattedPlayer = `Player ${playerId}`;
                if (playerId === userId.value) {
                    const choice = player.choice || '-';
                    formattedPlayer += ` (You: ${choice})`;
                }
                return formattedPlayer;
            });
        });

        const checkPlayerChoices = async () => {
            try {
                const response = await axios.get(`/get_lobby/${lobbyId.value}`);
                const lobbyData = response.data;

                const currentPlayer = lobbyData.players.find(player => player.user_id === userId.value);
                const opponent = lobbyData.players.find(player => player.user_id !== userId.value);

                const currentPlayerChoice = currentPlayer.choice;
                const opponentChoice = opponent.choice;

                if (!currentPlayerChoice && opponentChoice !== null) {
                    await axios.post(`/surrender_game/${lobbyId.value}/${opponent.user_id}`);
                    await leaveLobby();
                } else if (currentPlayerChoice !== null && !opponentChoice) {
                    await axios.post(`/surrender_game/${lobbyId.value}/${userId.value}`);
                    await router.push('/game');
                    await leaveLobby();
                } else if (!currentPlayerChoice && opponentChoice === null) {
                    await router.push('/game');
                    await leaveLobby();
                } else {
                    const response = await axios.get(`/check_winner/${lobbyId.value}`);
                    winner.value = response.data.winner;
                    if (winner.value !== 'waiting') {
                        await startRematchTimer();
                    }
                }
            } catch (error) {
                console.error('Failed to check player choices:', error);
                await leaveLobby();
            }
        };

        const requestRematch = async () => {
            try {
                await axios.post(`/confirm_rematch/${lobbyId.value}/${userId.value}`, null, {
                    params: {rematch_accepted: true}
                });
            } catch (error) {
                console.error('Failed to request rematch:', error);
                await router.push('/game');
                await axios.delete(`/delete_lobby/${lobbyId.value}`);
            }
        };

        const startRematchTimer = async () => {
            let countdown = 10;
            timerCountdown.value = timerSeconds;
            timerVisible.value = true;

            interval = setInterval(async () => {
                countdown--;
                if (countdown <= 0) {
                    clearInterval(interval);
                    await checkPlayerChoicesAfterRematch();
                    timerVisible.value = false;
                }
            }, 1000);
        }

        const checkPlayerChoicesAfterRematch = async () => {
            try {
                const response = await axios.get(`/get_lobby/${lobbyId.value}`);
                const lobbyData = response.data;

                const currentPlayer = lobbyData.players.find(player => player.user_id === userId.value);
                const opponent = lobbyData.players.find(player => player.user_id !== userId.value);

                const currentPlayerChoice = currentPlayer.choice;
                const opponentChoice = opponent.choice;

                if (currentPlayerChoice === null && opponentChoice === null) {
                    await router.push('/game');
                    await router.push({name: 'Lobby', params: {lobbyId: lobbyId.value}});
                } else {
                    await leaveLobby();
                }
            } catch (error) {
                console.error('Failed to check player choices after rematch:', error);
                await leaveLobby();
            }
        };

        const makeChoice = async (choice) => {
            try {
                const url = `/make_choice/${lobbyId.value}?current_user_id=${userId.value}&choice=${choice}`;
                await axios.post(url);
            } catch (error) {
                console.error('Failed to make choice:', error);
                throw error;
            }
        };

        const leaveLobby = async () => {
            try {
                await router.push('/game');
                await axios.delete(`/delete_lobby/${lobbyId.value}`);
            } catch (error) {
                console.error('Failed to leave lobby:', error);
            }
        };

        const winnerIdOrTie = computed(() => {
            if (winner.value === 'player1') {
                return players.value[0].user_id;
            } else if (winner.value === 'player2') {
                return players.value[1].user_id;
            } else {
                return 'tie';
            }
        });

        const result = computed(() => {
            if (winnerIdOrTie.value === userId.value) {
                return 'You win';
            } else if (winnerIdOrTie.value === 'tie') {
                return 'It\'s a tie';
            } else {
                return 'You lose';
            }
        });

        const startAfkTimer = () => {
            lobbyInterval.value = setInterval(() => {
                timerCountdown.value--;
                if (timerCountdown.value <= 0) {
                    clearInterval(lobbyInterval.value);
                    checkPlayerChoices();
                    timerVisible.value = false;
                }
            }, 1000);
        };

        onMounted(() => {
            startAfkTimer();
        });

        onBeforeUnmount(() => {
            clearInterval(interval);
            clearInterval(lobbyInterval);
        });

        return {
            lobbyId,
            userId,
            handleLobbyResponse,
            formattedPlayers,
            makeChoice,
            leaveLobby,
            requestRematch,
            winner,
            winnerIdOrTie,
            timerText,
            timerVisible,
            result
        };
    }
};
