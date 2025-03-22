import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status

from backend.secure.auth import SECRET_KEY, ALGORITHM
from backend.service import logger

router = APIRouter()
logger = logger.get_logger()


async def get_current_user_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing"
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")
        role = payload.get("role")
        if user_id is None or username is None or role is None:
            await websocket.close(code=1008)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        return {"user_id": user_id, "username": username, "role": role}
    except jwt.PyJWTError:
        await websocket.close(code=1008)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("New connection accepted. Total connections: %d", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("Connection disconnected. Total connections: %d", len(self.active_connections))

    async def broadcast(self, message: str):
        logger.info("Broadcasting message: %s", message)
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("WS connection attempt")
    current_user = await get_current_user_ws(websocket)
    logger.info("WS connected as %s", current_user)
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info("Received from %s: %s", current_user['username'], data)
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        logger.info("User %s disconnected", current_user['username'])
        manager.disconnect(websocket)
