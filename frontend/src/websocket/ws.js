let ws = null;
let reconnectTimeout = null;

const createWebSocket = () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        console.warn("❌ No token found. WebSocket won't connect.");
        return;
    }

    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = window.location.hostname;
    const wsPort = '8000'; // порт бэкенда
    const wsUrl = `${wsProtocol}//${wsHost}:${wsPort}/ws?token=${token}`;

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log("✅ WebSocket connection established");
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            console.log("📩 Received WS message:", data);
            document.dispatchEvent(new CustomEvent("wsMessage", { detail: data }));
        } catch (error) {
            console.error("⚠️ Error parsing WebSocket message:", error);
        }
    };

    ws.onerror = (error) => {
        console.error("❌ WebSocket error:", error);
    };

    ws.onclose = () => {
        console.log("⚠️ WebSocket connection closed");

        // Если токен все еще есть — пробуем переподключиться
        if (localStorage.getItem('access_token')) {
            console.log("🔄 Attempting WebSocket reconnect in 3 seconds...");
            reconnectTimeout = setTimeout(createWebSocket, 3000);
        }
    };
};

const closeWebSocket = () => {
    if (ws) {
        console.log("🔌 Closing WebSocket connection...");
        ws.close();
        ws = null;
        clearTimeout(reconnectTimeout);
    }
};

// **Следим за изменением `localStorage`**
window.addEventListener("storage", (event) => {
    if (event.key === "access_token") {
        if (!event.newValue) {
            console.log("🛑 Token removed, closing WebSocket...");
            closeWebSocket();
        } else if (!ws || ws.readyState !== WebSocket.OPEN) {
            console.log("🔄 Token added, creating WebSocket...");
            createWebSocket();
        }
    }
});

// **Следим за разрывом соединения перед выходом со страницы**
window.addEventListener("beforeunload", () => {
    closeWebSocket();
});

// **Запускаем WebSocket при загрузке страницы**
if (localStorage.getItem("access_token")) {
    createWebSocket();
}

export { createWebSocket, closeWebSocket };
