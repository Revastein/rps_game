import { ref, computed, onUnmounted } from "vue";
import axios from "axios";

export default {
    setup() {
        const searchingForOpponent = ref(false);
        const queueTimer = ref(0);
        let queueInterval = null;

        const currentPlayer = ref({
            id: null,
            username: "",
            rating: 0,
            games_played: 0,
            wins: 0,
            losses: 0,
            ties: 0,
            status: "idle", // 👈 Добавили статус игрока
        });

        const leaderboard = ref([]);

        const currentPlayerPosition = computed(() => {
            return leaderboard.value.findIndex(player => player.rating <= currentPlayer.value.rating) + 1;
        });

        const getAuthHeaders = () => {
            const token = localStorage.getItem("access_token");
            if (!token) {
                console.error("❌ No token found. Redirecting to login...");
                localStorage.removeItem("access_token");
                localStorage.removeItem("user_id");
                window.location.href = "/login";
                return null;
            }
            return { Authorization: `Bearer ${token}` };
        };

        // **Получение данных игрока (включая статус)**
        const fetchPlayerData = async () => {
            try {
                const userId = localStorage.getItem("user_id");
                const headers = getAuthHeaders();
                if (!userId || !headers) return;

                const response = await axios.get(`/user/${userId}`, { headers });
                if (response.data) {
                    currentPlayer.value = {
                        username: response.data.username,
                        rating: response.data.rating,
                        games_played: response.data.games_played,
                        wins: response.data.wins,
                        losses: response.data.losses,
                        ties: response.data.ties,
                        status: response.data.status || "idle", // 👈 Теперь статус приходит с API
                    };

                    // Обновляем состояние кнопки
                    searchingForOpponent.value = currentPlayer.value.status === "in_queue";
                }
            } catch (error) {
                console.error("❌ Error fetching player data:", error);
                window.location.href = "/login";
            }
        };

        // **Получение таблицы лидеров**
        const fetchLeaderboard = async () => {
            try {
                const headers = getAuthHeaders();
                if (!headers) return;

                const response = await axios.get("/users/", { headers });

                leaderboard.value = response.data
                    .sort((a, b) => b.rating - a.rating)
                    .slice(0, 5);
            } catch (error) {
                console.error("❌ Error fetching leaderboard:", error);
            }
        };

        // **Вход в очередь**
        const startGame = async () => {
            try {
                const userId = localStorage.getItem("user_id");
                const headers = getAuthHeaders();
                if (!userId || !headers) return;

                searchingForOpponent.value = true;
                queueTimer.value = 0;

                queueInterval = setInterval(() => {
                    queueTimer.value++;
                }, 1000);

                const response = await axios.post("/join_queue", { user_id: userId }, { headers });

                if (response.data) {
                    console.log("✅ Successfully joined the queue.");
                    currentPlayer.value.status = "in_queue";
                }
            } catch (error) {
                console.error("❌ Error joining queue:", error);
                searchingForOpponent.value = false;
                if (queueInterval) clearInterval(queueInterval);
            }
        };

        // **Выход из очереди**
        const leaveQueue = async () => {
            try {
                const userId = localStorage.getItem("user_id");
                const headers = getAuthHeaders();
                if (!userId || !headers) return;

                const response = await axios.delete("/delete_user_from_queue", {
                    headers,
                    data: { user_id: userId }
                });

                if (response.data.message === "Successfully left the queue") {
                    searchingForOpponent.value = false;
                    currentPlayer.value.status = "idle";
                    if (queueInterval) clearInterval(queueInterval);
                }
            } catch (error) {
                console.error("❌ Error leaving queue:", error);
            }
        };

        // **Обработка WebSocket событий**
        const handleWebSocketMessage = (event) => {
            const data = event.detail;
            console.log("📩 WebSocket event:", data);

            if (data.type === "status_update") {
                currentPlayer.value.status = data.status;
                console.log(`🔄 Updated status to: ${data.status}`);

                searchingForOpponent.value = currentPlayer.value.status === "in_queue";

                if (data.status === "in_lobby") {
                    console.log("🎮 Redirecting to lobby...");
                    window.location.href = "/lobby"; // Перенаправляем в лобби
                }
            }
        };

        // **Очистка таймера при выходе**
        onUnmounted(() => {
            if (queueInterval) clearInterval(queueInterval);
            document.removeEventListener("wsMessage", handleWebSocketMessage);
        });

        // **Загружаем данные при инициализации**
        fetchPlayerData();
        fetchLeaderboard();
        document.addEventListener("wsMessage", handleWebSocketMessage);

        return {
            searchingForOpponent,
            queueTimer,
            currentPlayer,
            leaderboard,
            currentPlayerPosition,
            startGame,
            leaveQueue,
        };
    }
};
